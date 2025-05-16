# from transformers import AutoModelForCausalLM, AutoTokenizer
# from peft import PeftModel, PeftConfig
# import torch
from transformers import BitsAndBytesConfig
#
# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM
# #
# # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# # model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
# # 设置路径
# base_model_path = "./Meta_Llama_3_8B2"  # 例如 "./llama-3-12b"
# finetuned_model_path = "./llama3_lora_finetuned"
#
# # 加载基础模型
# print("Loading base model...")
# bnb_config = BitsAndBytesConfig(load_in_8bit=True)
# model = AutoModelForCausalLM.from_pretrained(
#     base_model_path,
#     # device_map={"": "cpu"},
#     device_map="auto",
#     offload_folder="offload",
#     quantization_config=bnb_config,
#     # no_split_module_classes=["LlamaDecoderLayer"]
# )
# # 加载微调后的 LoRA 权重
# print("Loading fine-tuned LoRA weights...")
# # peft_config = PeftConfig.from_pretrained(finetuned_model_path)
# # model = PeftModel.from_pretrained(model, finetuned_model_path)
#
# # 加载分词器
# tokenizer = AutoTokenizer.from_pretrained(base_model_path)
#
# # 测试生成函数
# def generate_response(prompt, model, tokenizer, max_new_tokens=50):
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=max_new_tokens,
#             do_sample=True,
#             temperature=0.7,
#             top_k=50,
#             top_p=0.9,
#             pad_token_id=tokenizer.pad_token_id
#         )
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)
#
# # 示例测试
# # prompt = "who are you?"
# # # response = generate_response(prompt, model, tokenizer)
# # print("Prompt:", prompt)
# # print("Response:", response)
# input_text='who are you?'
# inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
# outputs = model.generate(**inputs, max_new_tokens=50)
#
#
# print("Generated text:")
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
# 设置原始模型路径
base_model_path = "./Meta_Llama_3_8B2"  # 修改为你的实际模型路径
# finetuned_model_path = "./llama3_lora_finetuned"
# finetuned_model_path = "./lora_output3"

finetuned_model_path = "./lora_function_calling"
# 加载基础模型
print("Loading base model...")
# model = AutoModelForCausalLM.from_pretrained(
#     base_model_path,
#     device_map="auto"  # 自动分配设备
# )
bnb_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    # device_map={"": "cpu"},
    device_map="auto",
    offload_folder="offload",
    quantization_config=bnb_config,
    # no_split_module_classes=["LlamaDecoderLayer"]
)

print("Loading fine-tuned LoRA weights...")
model = PeftModel.from_pretrained(model, finetuned_model_path, is_trainable=False)

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(finetuned_model_path)
# 加载分词器
# tokenizer = AutoTokenizer.from_pretrained(base_model_path)
print(model.peft_config["default"])
# 定义测试函数
def generate_response(prompt, model, tokenizer, max_new_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)  # 将输入转移到模型所在设备
    with torch.no_grad():  # 禁用梯度计算以节省内存
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,  # 最大生成的 token 数
            do_sample=True,                # 随机采样模式
            temperature=0.5,               # 控制生成的随机性
            top_k=50,                      # 限制前 k 个最高概率的词
            top_p=0.9,                     # 基于累积概率进行采样
            pad_token_id=tokenizer.pad_token_id  # 填充的 token ID
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)  # 解码生成的文本

# 测试输入
prompt = "What is the phosphorus content in Tokyo, Japan?"
response = generate_response(prompt, model, tokenizer)
print("Prompt:", prompt)
print("Response:", response)