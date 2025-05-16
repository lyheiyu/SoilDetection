import pandas as pd

df = pd.read_parquet("hf://datasets/Prazzwal07/soil_data/data/train-00000-of-00001.parquet")
# save df to csv
df.to_csv("soil_data.csv", index=False)

# import pandas as pd
#
# df = pd.read_parquet("hf://datasets/Prazzwal07/soil_data/data/train-00000-of-00001.parquet")
# # save df to csv
# df.to_csv("soil_data.csv", index=False)

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
# 加载数据集
dataset = load_dataset("YuvrajSingh9886/Agriculture-Soil-QA-Pairs-Dataset")
print(dataset)
# split dataset
# 按比例划分训练集和测试集
split_datasets = dataset["train"].train_test_split(test_size=0.2, seed=42)
print(split_datasets)
tokenizer = AutoTokenizer.from_pretrained("ehristoforu/llama-3-12b-instruct")
# 数据预处理
def preprocess_function(examples):
    inputs = examples["QUESTION.question"]
    targets = examples["ANSWER"]
    return tokenizer(inputs, text_target=targets, truncation=True, max_length=512)

tokenized_datasets = split_datasets.map(preprocess_function, batched=True)
train_dataset = tokenized_datasets["train"],
eval_dataset = tokenized_datasets["test"]
print(train_dataset[0])
print(eval_dataset[10])
# 配置训练
