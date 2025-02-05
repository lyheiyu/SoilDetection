from huggingface_hub import login
from transformers import AutoModel, AutoTokenizer
# model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
import torch
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
# model = AutoModel.from_pretrained(model_name, use_auth_token=True)
# #download model for hugging face
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
#
# # Specify the directory to save the tokenizer and model
# save_directory = "./meta_llama_3_8B2"
#
# # Save the tokenizer and model locally
# tokenizer.save_pretrained(save_directory)
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
import pandas as pd
import torch
from datasets import load_dataset,Dataset,DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer,
)
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
# model.save_pretrained(save_directory)
def generate_response(prompt, model, tokenizer, max_new_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 示例测试
prompt = "What is the best soil for growing wheat?"
response = generate_response(prompt, model, tokenizer)
print("Prompt:", prompt)
print("Response:", response)