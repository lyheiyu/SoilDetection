import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
# 1️⃣ 加载 LLaMA 模型
# ✅ 2️⃣ 读取土壤 pH 数据
json_file = "ireland_soil_ph_data.json"
with open(json_file, "r") as f:
    soil_data = json.load(f)

# ✅ 3️⃣ 定义查询函数
def get_soil_ph(latitude, longitude):
    """从 JSON 文件查询 pH 值"""
    for entry in soil_data:
        if round(entry["latitude"], 3) == round(latitude, 3) and round(entry["longitude"], 3) == round(longitude, 3):
            return entry["ph_h2o"]
    return "Data not found"

model_name = "./function_call3"  # 你可以使用本地路径
tokenizer = AutoTokenizer.from_pretrained(model_name)
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_8bit=True)
# model = AutoModelForCausalLM.from_pretrained(
#   "./llama-3-12b-local/",
#     # device_map={"": "cpu"},
#     device_map="auto",
#     offload_folder="offload",
#     quantization_config=bnb_config,
#     # no_split_module_classes=["LlamaDecoderLayer"]
# )
base_model_path = "./Meta_Llama_3_8B2"  # 修改为你的实际模型路径
# finetuned_model_path = "./llama3_lora_finetuned"
# finetuned_model_path = "./lora_output3"

finetuned_model_path = "./function_call3"
# 加载基础模型
print("Loading base model...")
# model = AutoModelForCausalLM.from_pretrained(
#     base_model_path,
#     device_map="auto"  # 自动分配设备
# )
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

# 2️⃣ 加载土壤数据
json_file = "ireland_soil_ph_data.json"
with open(json_file, "r") as f:
    soil_data = json.load(f)


# 3️⃣ 查询 pH 值的函数
def get_ph_value(latitude, longitude):
    """从 JSON 文件查询 pH 值"""
    for entry in soil_data:
        if round(entry["latitude"], 3) == round(latitude, 3) and round(entry["longitude"], 3) == round(longitude, 3):
            return entry["ph_h2o"]
    return "Data not found"

def clean_llama_output(output_text):
    """清理 LLaMA 生成的非 JSON 代码"""
    if "{" in output_text:
        output_text = output_text[output_text.index("{"):]  # 保留从 `{` 开始的部分
    if "}" in output_text:
        output_text = output_text[:output_text.rindex("}")+1]  # 保留到 `}` 结束
    return output_text.strip()
# 4️⃣ 让 LLaMA 生成 JSON 格式的函数调用
def llama_generate_function_call(prompt):
    """使用 LLaMA 解析 JSON 并返回"""
    input_text = f"""


    User request: "{prompt}"

    Function call (JSON only):
    """

    # ✅ 确保 tokenizer 具有 `pad_token`
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ✅ Tokenize 输入
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=254  # 限制长度，避免输出被截断
    )

    input_ids = inputs["input_ids"].to(model.device)
    attention_mask = inputs["attention_mask"].to(model.device)

    # ✅ 设置 pad_token_id
    model.config.pad_token_id = tokenizer.pad_token_id

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,  # ✅ 解决 `attention_mask` 相关警告
            max_length=256,  # ✅ 限制生成长度，防止 JSON 不完整
            temperature=0.5,
            do_sample=False,  # ✅ 关闭随机采样，确保输出稳定
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    output_text = clean_llama_output(output_text)
    print(output_text)
    # ✅ 解析 JSON
    try:
        function_call = json.loads(output_text.strip())
        print(function_call)
        return function_call
    except json.JSONDecodeError:
        print("⚠️ LLaMA 生成的输出无法解析为 JSON！")
        print("🔍 生成的内容:", output_text)
        return {"error": "Invalid function call format"}


# 5️⃣ 处理 LLaMA 生成的函数调用
def process_function_call(prompt):
    """解析 LLaMA 生成的 JSON，并执行查询"""
    function_call = llama_generate_function_call(prompt)

    if "error" in function_call:
        return function_call["error"]

    if function_call["name"] == "get_soil_ph":
        args = function_call["arguments"]
        lat, lon = args["latitude"], args["longitude"]
        ph_value = get_soil_ph(lat, lon)
        return f"The soil pH at latitude {lat}, longitude {lon} is: {ph_value}"

    return "Function call not recognized."


# 6️⃣ 交互模式
while True:
    user_input = input("Enter coordinates (e.g., 'What is the soil pH at latitude 53.3 longitude -6.2?'): ")
    print(1)
    if user_input.lower() in ["exit", "quit"]:
        break
    print(process_function_call(user_input))
