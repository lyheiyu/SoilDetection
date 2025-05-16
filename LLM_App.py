import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from transformers import BitsAndBytesConfig

# **初始化 Streamlit 页面**
st.set_page_config(page_title="Soil AI Chatbot", layout="centered")
st.title("🌱 Soil AI Chatbot")
st.markdown("Ask a question about soil and get an AI-generated answer!")

# **加载模型**
@st.cache_resource()  # 使用 Streamlit 缓存机制，避免重复加载
def load_model():
    base_model_path = "./Meta_Llama_3_8B2"  # 你的 LLaMA3 8B 模型路径
    finetuned_model_path = "./lora_output"  # 你的 LoRA 微调模型路径

    bnb_config = BitsAndBytesConfig(load_in_8bit=True)

    print("Loading base model...")

    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        device_map="auto",
        quantization_config=bnb_config
    )

    print("Loading fine-tuned LoRA weights...")
    model = PeftModel.from_pretrained(model, finetuned_model_path)

    tokenizer = AutoTokenizer.from_pretrained(finetuned_model_path)

    return model, tokenizer

# **加载模型**
model, tokenizer = load_model()

# **定义生成回答函数**
def generate_response(prompt, max_new_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.5,
            top_k=50,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# **用户输入框**
user_input = st.text_area("Enter your question here:", "")

if st.button("Generate Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Generating answer... ⏳"):
            response = generate_response(user_input)
        st.success("AI Response:")
        st.write(response)
