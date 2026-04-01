import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# -------------------------------
# 🧠 Model Configuration
# -------------------------------
MODEL_NAME = "meta-llama/Llama-3-8b-instruct"  # change if needed

print("🔄 Loading LLaMA model (LLM Service)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("✅ LLaMA model loaded successfully!")

# -------------------------------
# 💬 Generate Response
# -------------------------------
def generate_llm_response(prompt: str) -> str:
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.1
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean response (remove prompt echo)
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        return response

    except Exception as e:
        return f"Error generating response: {str(e)}"
