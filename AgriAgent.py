import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# ========== 1) 配置模型 & 量化 & 路径 ==========
base_model_path = "./Meta_Llama_3_8B2"  # 你的基础模型路径 (示例)
finetuned_model_path = "./function_call2"  # 你微调/LoRA 输出路径 (示例)

bnb_config = BitsAndBytesConfig(load_in_8bit=True)  # 8-bit 量化配置
device_map = "auto" if torch.cuda.is_available() else {"": "cpu"}

# ========== 2) 加载 Tokenizer ==========
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
# 如果你的 tokenizer 没有 pad_token，下面这行可以避免生成时出错
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ========== 3) 加载基础模型 + LoRA 权重 ==========
print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    device_map=device_map,
    quantization_config=bnb_config,  # 使用量化
    offload_folder="offload",        # 如果显存不足，可以设置offload文件夹
)

print("Loading fine-tuned LoRA weights...")
model = PeftModel.from_pretrained(
    base_model,
    finetuned_model_path,
    is_trainable=False
)

# 将模型切换到推理模式
model.eval()

print("模型PEFT配置信息:", model.peft_config["default"])

# ========== 4) 加载土壤 pH 数据 ==========
json_file = "ireland_soil_ph_data.json"
with open(json_file, "r") as f:
    soil_data = json.load(f)

def get_soil_ph(latitude, longitude):
    """从 JSON 文件中查询 pH 值"""
    for entry in soil_data:
        # 这里用 round(..., 3) 做简单的坐标匹配
        if round(entry["latitude"], 3) == round(latitude, 3) and round(entry["longitude"], 3) == round(longitude, 3):
            return entry["ph_h2o"]
    return "Data not found"

# ========== 5) 工具函数：清理/解析模型输出 ==========
def clean_llama_output(output_text):
    """
    尝试从模型输出中截取第一个完整的 { ... } JSON。
    如果模型输出中包含多余的文本或换行，就做简单剪切。
    """
    if "{" in output_text:
        output_text = output_text[output_text.index("{"):]
    if "}" in output_text:
        output_text = output_text[:output_text.rindex("}")+1]
    return output_text.strip()

def llama_generate_function_call(prompt):
    """
    让模型输出 JSON 格式的函数调用信息:
    例如:
    {
      "name": "get_soil_ph",
      "arguments": {
         "latitude": 53.3,
         "longitude": -6.2
      }
    }
    """
    # 在 Prompt 中引导模型只生成 JSON
    system_prompt = (
        "You are a helpful assistant. The user wants to call a function to get the soil pH.\n"
        "You MUST return only valid JSON with the following schema:\n"
        "{\n"
        "   \"name\": \"get_soil_ph\",\n"
        "   \"arguments\": {\n"
        "       \"latitude\": <float>,\n"
        "       \"longitude\": <float>\n"
        "   }\n"
        "}\n\n"
        "Do not add any extra keys. Do not add additional text outside of this JSON.\n"
    )

    full_prompt = f"{system_prompt}\nUser request: \"{prompt}\"\nFunction call (JSON only):"

    inputs = tokenizer(
        full_prompt,
        return_tensors="pt",
        padding="longest",
        truncation=True,
        max_length=512
    )
    input_ids = inputs["input_ids"].to(model.device)
    attention_mask = inputs["attention_mask"].to(model.device)

    # 强制让模型使用pad_token_id，避免警告
    model.config.pad_token_id = tokenizer.pad_token_id

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=256,
            temperature=0.0,   # 建议温度低一些，尽量保持 deterministic
            do_sample=False,   # 关闭采样，减少随机性
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # 清理出JSON
    json_str = clean_llama_output(output_text)
    try:
        function_call = json.loads(json_str)
        return function_call
    except json.JSONDecodeError:
        print("⚠️ 无法解析JSON，生成的文本如下：")
        print(output_text)
        return {"error": "Invalid JSON format", "raw": output_text}

def process_function_call(prompt):
    """
    1. 让模型生成JSON函数调用描述
    2. 如果函数是 get_soil_ph，就执行查询
    """
    function_call = llama_generate_function_call(prompt)
    if "error" in function_call:
        return f"Error: {function_call['error']}"

    if function_call.get("name") == "get_soil_ph":
        args = function_call.get("arguments", {})
        latitude = args.get("latitude")
        longitude = args.get("longitude")
        if latitude is not None and longitude is not None:
            ph_value = get_soil_ph(latitude, longitude)
            return f"The soil pH at latitude {latitude}, longitude {longitude} is: {ph_value}"
        else:
            return "Invalid arguments: latitude or longitude missing."
    else:
        return "Unknown function call."

# ========== 6) 简单的交互式测试 ==========
def main():
    print("\n=== Soil pH Query Assistant ===")
    print("Example: 'What is the soil pH at latitude 53.3 and longitude -6.2?'\n")
    while True:
        user_input = input("User: ")
        if user_input.lower().strip() in ["exit", "quit", "q"]:
            break
        response = process_function_call(user_input)
        print("Assistant:", response, "\n")

if __name__ == "__main__":
    main()
