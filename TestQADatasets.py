from datasets import load_dataset

# # 加载数据集
# dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
# # 查看数据集结构
# print(dataset)
# # 查看数据集中的train length
# print(len(dataset["train"]))
# print(dataset["train"][0])
import os
# from datasets import load_dataset
# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     TrainingArguments,
#     Trainer,
# )
# from peft import LoraConfig, get_peft_model, TaskType
# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM
#
# tokenizer = AutoTokenizer.from_pretrained("ehristoforu/llama-3-12b-instruct")
# model = AutoModelForCausalLM.from_pretrained("ehristoforu/llama-3-12b-instruct")
# # 1. 加载模型和分词器
# # model_name = "llama3:8b"  # 替换为你的 LLaMA3 模型名称
# output_dir = "./llama3_lora_finetuned"
#
# print("Loading tokenizer and model...")
# # tokenizer = AutoTokenizer.from_pretrained(model_name)
# # model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
#
# # 2. 加载数据集
# print("Loading dataset...")
# dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
#
# # 3. 数据预处理
# def preprocess_function(examples):
#     inputs = examples["QUESTION.question"]
#     targets = examples["ANSWER"]
#     return tokenizer(inputs, text_target=targets, truncation=True, max_length=512)
#
# print("Preprocessing dataset...")
# tokenized_datasets = dataset.map(preprocess_function, batched=True)
#
# # 4. 配置 LoRA
# print("Configuring LoRA...")
# lora_config = LoraConfig(
#     task_type=TaskType.CAUSAL_LM,  # 因果语言模型任务
#     r=16,
#     lora_alpha=32,
#     lora_dropout=0.1
# )
# model = get_peft_model(model, lora_config)
# model.print_trainable_parameters()
#
# # 5. 配置训练参数
# print("Setting up training arguments...")
# training_args = TrainingArguments(
#     output_dir=output_dir,
#     per_device_train_batch_size=4,  # 根据显存调整
#     num_train_epochs=3,  # 训练轮数
#     learning_rate=2e-4,  # 学习率
#     save_strategy="epoch",  # 每个 epoch 保存
#     evaluation_strategy="epoch",  # 每个 epoch 评估
#     logging_dir="./logs",
#     fp16=True,  # 启用混合精度
#     save_total_limit=2  # 最多保存两个模型
# )
#
# # 6. 开始训练
# print("Starting training...")
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_datasets["train"],
#     eval_dataset=tokenized_datasets["test"]
# )
#
# trainer.train()
#
# # 7. 保存微调后的模型
# print("Saving fine-tuned model...")
# model.save_pretrained(output_dir)
# tokenizer.save_pretrained(output_dir)
#
# # 8. 测试生成
# print("Testing fine-tuned model...")
# input_text = "What is the best soil for growing wheat?"
# inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
# outputs = model.generate(**inputs, max_new_tokens=50)
# print("Generated text:")
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# import torch
#
# print("CUDA available:", torch.cuda.is_available())
# print("GPU count:", torch.cuda.device_count())
# if torch.cuda.is_available():
#     print("GPU name:", torch.cuda.get_device_name(0))

#
# # 1. 加载模型和分词器
# # model_name = "llama3:8b"  # 替换为你的 LLaMA3 模型名称
# output_dir = "./llama3_lora_finetuned"
#
# print("Loading tokenizer and model...")
# # tokenizer = AutoTokenizer.from_pretrained(mode.l_name)
# # model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
#
# # 2. 加载数据集
# print("Loading dataset...")
# dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
# split_datasets = dataset["train"].train_test_split(test_size=0.2, seed=42)

# 3. 数据预处理
# def preprocess_function(examples):
#     inputs = examples["QUESTION.question"]
#     targets = examples["ANSWER"]
#     return tokenizer(inputs, text_target=targets, truncation=True, max_length=512)
#
# print("Preprocessing dataset...")
# tokenized_datasets = split_datasets.map(preprocess_function, batched=True)
#
#
# # 4. 配置 LoRA
# print("Configuring LoRA...")
# lora_config = LoraConfig(
#     task_type=TaskType.CAUSAL_LM,  # 因果语言模型任务
#     r=16,
#     lora_alpha=32,
#     lora_dropout=0.1
# )
# model = get_peft_model(model, lora_config)
# model.print_trainable_parameters()
#
# # 5. 配置训练参数
# print("Setting up training arguments...")
# training_args = TrainingArguments(
#     output_dir=output_dir,
#     per_device_train_batch_size=4,  # 根据显存调整
#     num_train_epochs=3,  # 训练轮数
#     learning_rate=2e-4,  # 学习率
#     save_strategy="epoch",  # 每个 epoch 保存
#     evaluation_strategy="epoch",  # 每个 epoch 评估
#     logging_dir="./logs",
#     fp16=True,  # 启用混合精度
#     save_total_limit=2  # 最多保存两个模型
# )
#
# # 6. 开始训练
# print("Starting training...")
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_datasets["train"],
#     eval_dataset=tokenized_datasets["test"]
# )
#
# trainer.train()
#
# # 7. 保存微调后的模型
# print("Saving fine-tuned model...")
# model.save_pretrained(output_dir)
# tokenizer.save_pretrained(output_dir)
#
# # 8. 测试生成
# print("Testing fine-tuned model...")
# input_text = "What is the best soil for growing wheat?"
# inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
# outputs = model.generate(**inputs, max_new_tokens=50)
# print("Generated text:")
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# def preprocess_function(examples):
#     inputs = examples["QUESTION.question"]
#     targets = examples["ANSWER"]
#     model_inputs = tokenizer(
#         inputs, max_length=512, truncation=True, padding="max_length"
#     )
#     labels = tokenizer(
#         targets, max_length=512, truncation=True, padding="max_length"
#     )
#     model_inputs["labels"] = labels["input_ids"]
#     return model_inputs
#
# tokenized_datasets = split_datasets.map(preprocess_function, batched=True)
#
# # 4. 配置 LoRA
# lora_config = LoraConfig(
#     task_type=TaskType.CAUSAL_LM, r=16, lora_alpha=32, lora_dropout=0.1
# )
# model = get_peft_model(model, lora_config)
# model.print_trainable_parameters()
#
# # 5. 创建数据填充器
# data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
#
# # 6. 配置训练参数
# training_args = TrainingArguments(
#     output_dir="./llama3_lora_finetuned",
#     per_device_train_batch_size=4,
#     num_train_epochs=3,
#     learning_rate=2e-4,
#     save_strategy="epoch",
#     evaluation_strategy="epoch",
#     logging_dir="./logs",
#     fp16=True,
#     save_total_limit=2
# )
#
# # 7. 开始训练
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_datasets["train"],
#     eval_dataset=tokenized_datasets["test"],
#     data_collator=data_collator
# )
#
# trainer.train()
#
# # 8. 保存模型
# model.save_pretrained("./llama3_lora_finetuned")
# tokenizer.save_pretrained("./llama3_lora_finetuned")
from datasets import load_dataset,Dataset,DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer,
)
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
import pandas as pd
import torch

# 1. 加载数据集
# dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
# split_datasets = dataset["train"].train_test_split(test_size=0.2, seed=42)
file_path = "Datasets/qna-dataset-farmgenie-soil-v2.csv"  # 替换为你的本地文件路径
data = pd.read_csv(file_path)

# 只保留需要的列
filtered_data = data[['QUESTION.question', 'ANSWER']].dropna()

# 转换为 Hugging Face Dataset 格式
dataset = Dataset.from_pandas(filtered_data)
dataset_dict = DatasetDict({
    "train": dataset  # 将整个数据集初始化为训练集
})

# 划分训练集和测试集
split_datasets = dataset_dict["train"].train_test_split(test_size=0.2, seed=42)

# 查看分割后的数据集
print("训练集大小:", len(split_datasets["train"]))
print("测试集大小:", len(split_datasets["test"]))
# split_datasets = dataset["train"].train_test_split(test_size=0.2, seed=42)
# 查看处理后的数据集
print(dataset)
print(split_datasets)
for item in split_datasets:
    print(item)
# 保存为 Hugging Face Dataset 格式
dataset.save_to_disk("processed_dataset")
# 2. 加载分词器和模型
# tokenizer = AutoTokenizer.from_pretrained("ehristoforu/llama-3-12b-instruct")
# model = AutoModelForCausalLM.from_pretrained("ehristoforu/llama-3-12b-instruct")

# 保存模型和分词器
local_model_path = "./meta_llama_3_8B2"
# model.save_pretrained(local_model_path)
# tokenizer.save_pretrained(local_model_path)
with init_empty_weights():
    model = AutoModelForCausalLM.from_pretrained(local_model_path)

# 加载并分发权重
bnb_config = BitsAndBytesConfig(load_in_8bit=True)
# model = AutoModelForCausalLM.from_pretrained(
#   "./llama-3-12b-local/",
#     # device_map={"": "cpu"},
#     device_map="auto",
#     offload_folder="offload",
#     quantization_config=bnb_config,
#     # no_split_module_classes=["LlamaDecoderLayer"]
# )
model = AutoModelForCausalLM.from_pretrained(
  local_model_path,
    # device_map={"": "cpu"},
    device_map="auto",
    offload_folder="offload",
    quantization_config=bnb_config,
    # no_split_module_classes=["LlamaDecoderLayer"]
)

model.gradient_checkpointing_enable()
model.config.use_cache = False
# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(local_model_path)

# 检查分词器的特殊标记
if tokenizer.pad_token is None:
    if tokenizer.eos_token:
        tokenizer.pad_token = tokenizer.eos_token  # 设置 pad_token 为 eos_token
    else:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # 添加自定义 pad_token
        model.resize_token_embeddings(len(tokenizer))  # 更新模型词汇表
# 3. 数据预处理
# def preprocess_function(examples):
#     inputs = examples["QUESTION.question"]
#     targets = examples["ANSWER"]
#     return tokenizer(inputs, text_target=targets, truncation=True, max_length=512)
# tokenized_datasets = split_datasets.map(preprocess_function, batched=True)
def preprocess_function(examples):
    inputs = examples["QUESTION.question"]
    targets = examples["ANSWER"]

    # 对输入进行分词
    model_inputs = tokenizer(
        inputs,
        max_length=512,
        truncation=True,
        padding="max_length"  # 确保所有样本长度一致
    )

    # 对标签进行分词
    labels = tokenizer(
        targets,
        max_length=512,
        truncation=True,
        padding="max_length"  # 确保标签长度一致
    )["input_ids"]

    # 将填充值设置为 -100（用于忽略梯度计算）
    labels_with_ignore_index = [
        [-100 if token == tokenizer.pad_token_id else token for token in label]
        for label in labels
    ]

    model_inputs["labels"] = labels_with_ignore_index
    return model_inputs

# 应用数据预处理
tokenized_datasets = split_datasets.map(preprocess_function, batched=True)
# 4. 配置 LoRA
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
# 6. 配置训练参数
def compute_loss(model, inputs):
    outputs = model(**inputs)
    logits = outputs.logits
    labels = inputs["labels"]

    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()

    loss = F.cross_entropy(
        shift_logits.view(-1, shift_logits.size(-1)),
        shift_labels.view(-1),
        ignore_index=-100
    )
    return loss
from transformers import Trainer

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
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
# 配置训练参数
training_args = TrainingArguments(
    output_dir="./llama3_lora_finetuned",
    per_device_train_batch_size=2,
    num_train_epochs=10,
    learning_rate=2e-2,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_dir="./logs",
    fp16=False
)
optimizer = torch.optim.AdamW(
    filter(lambda p: p.requires_grad, model.parameters()), lr=2e-2
)
# 创建 Trainer
trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator
)

# 开始训练
trainer.train()

# 8. 保存模型
model.save_pretrained("./llama3_lora_finetuned")
tokenizer.save_pretrained("./llama3_lora_finetuned")