
import os
import pandas as pd
import torch
from torch.nn import functional as F
from datasets import Dataset, DatasetDict, load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType,PeftModel

###############################################################################
# 1. 加载与预处理数据
###############################################################################

# 假设你的CSV文件路径如下，包含 "QUESTION.question" 和 "ANSWER" 两列
file_path = "Datasets/qna-dataset-farmgenie-soil-v2.csv"  # 改成你的实际CSV路径
data = pd.read_csv(file_path)

# 丢弃空值行
data = data[['QUESTION.question', 'ANSWER']].dropna()

# 将数据转为 HF Dataset
dataset_hf = Dataset.from_pandas(data)

# 将整个数据集拆分为训练集和测试集
split_datasets = dataset_hf.train_test_split(test_size=0.1, seed=42)

print("训练集大小:", len(split_datasets["train"]))
print("测试集大小:", len(split_datasets["test"]))

# 在真实场景下，建议查看几条数据进行验证
print("样例数据:", split_datasets["train"][0])

###############################################################################
# 2. 加载模型与分词器（示例：openlm-research/open_llama_7b）
#    如果你有自己的本地模型，请替换 model_name 为对应路径
###############################################################################
# local_model_path = "./meta_llama_3_8B2"
model_name = "./meta_llama_3_8B2"  # 你可以换成自己的模型路径

# 配置 8-bit 量化
bnb_config = BitsAndBytesConfig(load_in_8bit=True)

# 加载分词器
# 对于很多 LLaMA/开源变体，需要指定 use_fast=False
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
# 可能需要添加trust_remote_code=True，视情况而定:
# tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, trust_remote_code=True)

# 加载 8-bit 量化的模型并映射到 GPU
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config
)

# 如果模型没有pad_token，手动添加
if tokenizer.pad_token is None:
    # 如果模型有 eos_token，就把pad_token设为eos_token
    if tokenizer.eos_token:
        tokenizer.pad_token = tokenizer.eos_token
    else:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))

# 可以开启 gradient checkpointing 以节省显存
model.gradient_checkpointing_enable()
model.config.use_cache = False  # 在训练中通常关闭 cache，以支持梯度检查点

###############################################################################
# 3. 配置 LoRA
###############################################################################

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"],  # 适用于 LLaMA
)

model = get_peft_model(model, lora_config)
# **检查所有参数的 requires_grad 状态**
for name, param in model.named_parameters():
    print(f"{name} - requires_grad: {param.requires_grad}")

# **检查 LoRA 层是否解冻**
trainable_params = [name for name, param in model.named_parameters() if param.requires_grad]
if len(trainable_params) == 0:
    raise ValueError(" 没有可训练参数，请检查 LoRA 是否正确应用！")

print(f" 发现 {len(trainable_params)} 个可训练参数！")
model = get_peft_model(model, lora_config)
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, r=16, lora_alpha=32, lora_dropout=0.1
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
from torch.nn import functional as F
# 5. 创建数据填充器
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding="longest")
for name, param in model.named_parameters():
    print(f"Parameter {name}: dtype={param.dtype}, requires_grad={param.requires_grad}")
    if param.dtype.is_floating_point or param.dtype.is_complex:
        param.requires_grad = True
# **确保 LoRA 层解冻**
for name, param in model.named_parameters():
    if "lora_" in name:
        param.requires_grad = True
# 打印可训练参数量
parametersforPrint=model.print_trainable_parameters()
print(parametersforPrint)
###############################################################################
# 4. 数据预处理函数：统一包装为 prompt & answer 格式
###############################################################################

def preprocess_function(examples):
    # 将问题/答案包装成指令样式，以帮助模型学到更好的上下文
    # 你可以根据自己需要，微调提示语的格式
    inputs = [
        f"Question: {q}\nAnswer:"
        for q in examples["QUESTION.question"]
    ]
    targets = examples["ANSWER"]

    # 分词输入
    model_inputs = tokenizer(
        inputs,
        max_length=512,
        truncation=True,
        padding="max_length"  # 确保所有样本长度一致
    )

    # 分词标签
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets,
            max_length=512,
            truncation=True,
            padding="max_length"
        )["input_ids"]

    # 将 pad_token_id 替换为 -100，以便在计算loss时忽略
    labels_with_ignore_index = []
    for label in labels:
        label = [
            (l if l != tokenizer.pad_token_id else -100) for l in label
        ]
        labels_with_ignore_index.append(label)

    model_inputs["labels"] = labels_with_ignore_index
    return model_inputs

# 应用数据预处理
tokenized_datasets = split_datasets.map(preprocess_function, batched=True)

###############################################################################
# 5. 创建 DataCollator
###############################################################################

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    padding="longest"
)

###############################################################################
# 6. 自定义 Trainer（可选，如果想在前向传播时手动移动 logits）
#    这里可以直接使用官方 Trainer + DataCollatorForLanguageModeling 也可以
###############################################################################

class CustomTrainer(Trainer):
    def compute_loss(
        self,
        model,
        inputs,
        return_outputs=False,
        **kwargs  # <--- 加上这个
    ):
        outputs = model(**inputs)
        logits = outputs.logits
        labels = inputs["labels"]

        # 移位 logits 和 labels 以对齐
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        # 计算交叉熵损失
        loss = F.cross_entropy(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
            ignore_index=-100
        )
        return (loss, outputs) if return_outputs else loss

###############################################################################
# 7. 配置训练参数
###############################################################################
save_model_pach="./lora_output3"
training_args = TrainingArguments(
    output_dir=save_model_pach,
    overwrite_output_dir=True,
    num_train_epochs=5,               # 先试5个epoch，可根据需要自行调整
    per_device_train_batch_size=2,    # 根据显存大小酌情调整
    per_device_eval_batch_size=2,
    learning_rate=2e-4,               # 建议LoRA场景下从1e-4 ~ 2e-4起试
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_dir="./logs",
    logging_steps=50,                 # 训练时多少step输出一次日志
    fp16=False,                       # 如果显存支持可以True，否则False
    # torch_compile=True,             # pytorch 2.0以上可以考虑开启编译
)

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator
)

###############################################################################
# 8. 开始训练
###############################################################################

trainer.train()

###############################################################################
# 9. 保存微调后模型（LoRA权重 + tokenizer）
###############################################################################
if not isinstance(model, PeftModel):
    raise ValueError("❌ 当前 `model` 不是 PeftModel，请检查 LoRA 适配器是否正确加载！")

model.save_pretrained(save_model_pach)
# trainer.save_model(save_model_pach)  # 等价于 model.save_pretrained(...)
tokenizer.save_pretrained(save_model_pach)

###############################################################################
# 10. 简单推理示例
#     加载微调后的模型权重，并输入一个测试问题，看输出效果
###############################################################################
print("\n=== Inference Test ===")

from transformers import GenerationConfig

# 再次加载LoRA微调后的模型
finetuned_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config
)
finetuned_model = get_peft_model(finetuned_model, lora_config)
finetuned_model.load_adapter(save_model_pach)  # 加载LoRA权重

# 构建Prompt
prompt = "Question: How to improve soil health?\nAnswer:"

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# 生成配置（可根据需要调整）
gen_config = GenerationConfig(
    max_new_tokens=128,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    eos_token_id=tokenizer.eos_token_id
)

# 推理
with torch.no_grad():
    generated_ids = finetuned_model.generate(
        **inputs,
        **gen_config.__dict__
    )
output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
print("Model Output:\n", output)
