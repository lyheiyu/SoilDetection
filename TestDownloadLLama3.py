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
#download model for hugging face
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
# Specify the directory to save the tokenizer and model
save_directory = "./DeepSeek-R1-Distill-Llama-8B"

# Save the tokenizer and model locally
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)
def generate_response(prompt, model, tokenizer, max_new_tokens=50):
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