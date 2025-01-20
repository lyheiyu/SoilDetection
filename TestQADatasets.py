from datasets import load_dataset

# # 加载数据集
# dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
# # 查看数据集结构
# print(dataset)
# # 查看数据集中的train length
# print(len(dataset["train"]))
# print(dataset["train"][0])
import os
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, TaskType
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("ehristoforu/llama-3-12b-instruct")
model = AutoModelForCausalLM.from_pretrained("ehristoforu/llama-3-12b-instruct")
# 1. 加载模型和分词器
# model_name = "llama3:8b"  # 替换为你的 LLaMA3 模型名称
output_dir = "./llama3_lora_finetuned"

print("Loading tokenizer and model...")
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# 2. 加载数据集
print("Loading dataset...")
dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")

# 3. 数据预处理
def preprocess_function(examples):
    inputs = examples["QUESTION.question"]
    targets = examples["ANSWER"]
    return tokenizer(inputs, text_target=targets, truncation=True, max_length=512)

print("Preprocessing dataset...")
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# 4. 配置 LoRA
print("Configuring LoRA...")
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,  # 因果语言模型任务
    r=16,
    lora_alpha=32,
    lora_dropout=0.1
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 5. 配置训练参数
print("Setting up training arguments...")
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=4,  # 根据显存调整
    num_train_epochs=3,  # 训练轮数
    learning_rate=2e-4,  # 学习率
    save_strategy="epoch",  # 每个 epoch 保存
    evaluation_strategy="epoch",  # 每个 epoch 评估
    logging_dir="./logs",
    fp16=True,  # 启用混合精度
    save_total_limit=2  # 最多保存两个模型
)

# 6. 开始训练
print("Starting training...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"]
)

trainer.train()

# 7. 保存微调后的模型
print("Saving fine-tuned model...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

# 8. 测试生成
print("Testing fine-tuned model...")
input_text = "What is the best soil for growing wheat?"
inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=50)
print("Generated text:")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
