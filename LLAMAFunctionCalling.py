import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType

###############################################################################
# 1. 加载与预处理数据
###############################################################################
# 训练数据路径
file_path = "synthetic_function_calling_train.csv"  # 你的 Function Calling 训练数据
data = pd.read_csv(file_path)

# 转换为 Hugging Face 数据格式
dataset_hf = Dataset.from_pandas(data)

# 拆分训练集和测试集
split_datasets = dataset_hf.train_test_split(test_size=0.1, seed=42)

print("训练集大小:", len(split_datasets["train"]))
print("测试集大小:", len(split_datasets["test"]))

###############################################################################
# 2. 加载 LLaMA 3 8B（量化 & 分词器）
###############################################################################
model_name = "./meta_llama_3_8B2"  # 你的 LLaMA 3 8B 模型路径

# 8-bit 量化配置
# bnb_config = BitsAndBytesConfig(load_in_8bit=True)
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.float16,  # 确保计算梯度
    bnb_8bit_use_double_quant=False  # 禁止 double quant 防止梯度丢失
)

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

# 加载 8-bit 量化模型
print("Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config
)

# 添加 padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 启用 Gradient Checkpointing 以节省显存
model.gradient_checkpointing_enable()
model.config.use_cache = False

###############################################################################
# 3. 配置 LoRA 适配器
###############################################################################
lora_config = LoraConfig(
    r=32,
    lora_alpha=32,
    lora_dropout=0.1,
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "v_proj"]
)

# 应用 LoRA 适配器
model = get_peft_model(model, lora_config)

# 确保 LoRA 层是可训练的
for name, param in model.named_parameters():
    print(f"Parameter {name}: dtype={param.dtype}, requires_grad={param.requires_grad}")
    if param.dtype.is_floating_point or param.dtype.is_complex:
        param.requires_grad = True
# **确保 LoRA 层解冻**
for name, param in model.named_parameters():
    if "lora_" in name:
        param.requires_grad = True
# for name, param in model.named_parameters():
#     print(f"{name}: requires_grad={param.requires_grad}")
# for name, param in model.named_parameters():
#     print(f"Parameter {name}: dtype={param.dtype}, requires_grad={param.requires_grad}")
#     if param.dtype.is_floating_point or param.dtype.is_complex:
#         param.requires_grad = True
# 检查 LoRA 适配器是否正确加载
trainable_params = [name for name, param in model.named_parameters() if param.requires_grad]
print(f"发现 {len(trainable_params)} 个可训练参数！")

###############################################################################
# 4. 预处理数据（格式化为 Prompt -> JSON 输出）
###############################################################################
def preprocess_function(examples):
    inputs = [f"Question: {q}\nAnswer (JSON format):" for q in examples["QUESTION.question"]]
    targets = examples["ANSWER"]

    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=512, truncation=True, padding="max_length")["input_ids"]

    # **确保 labels 正确设置**
    if labels is None or len(labels) == 0:
        raise ValueError("❌ `labels` 为空，请检查数据格式！")

    # **将 `pad_token_id` 替换为 -100**
    model_inputs["labels"] = [
        [(l if l != tokenizer.pad_token_id else -100) for l in label]
        for label in labels
    ]
    return model_inputs


# 应用数据预处理
tokenized_datasets = split_datasets.map(preprocess_function, batched=True)

###############################################################################
# 5. 训练参数配置
###############################################################################
save_model_path = "./lora_function_calling"

training_args = TrainingArguments(
    output_dir="./lora_output",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    learning_rate=2e-4,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_dir="./logs",
    logging_steps=50,
    bf16=True,
    fp16=False,  # ❌ 不能使用 FP16 训练，否则会触发 unscale FP16 gradients 错误
    optim="adamw_bnb_8bit",  # ✅ 8-bit 量化优化器
)
from torch.nn import functional as F
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        outputs = model(**inputs)
        logits = outputs.logits
        labels = inputs.get("labels")

        if labels is None:
            raise ValueError("❌ `labels` 为空，请检查数据格式！")

        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        loss = F.cross_entropy(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
            ignore_index=-100
        )

        # **手动检查 `loss.requires_grad`**
        if not loss.requires_grad:
            loss = loss.clone().detach().requires_grad_(True)  # ✅ 重新启用梯度

        return (loss, outputs) if return_outputs else loss




# 创建 Trainer
trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model, padding="longest")
)

###############################################################################
# 6. 开始训练
###############################################################################
trainer.train()

###############################################################################
# 7. 保存微调后的 LoRA 适配器
###############################################################################
print("Saving LoRA adapter...")
model.save_pretrained(save_model_path)
tokenizer.save_pretrained(save_model_path)
print(f"✅ LoRA 适配器已保存至 {save_model_path}")
