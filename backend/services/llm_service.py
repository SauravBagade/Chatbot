import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# -------------------------------
# 🧠 Model Configuration (LIGHT MODEL)
# -------------------------------
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("🔄 Loading LLaMA model (LLM Service)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,   # CPU safe
    device_map="cpu"             # force CPU
)

print("✅ Model loaded successfully!")

# -------------------------------
# 💬 Generate Response
# -------------------------------
def generate_llm_response(prompt: str) -> str:
    try:
        inputs = tokenizer(prompt, return_tensors="pt")

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean output
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        return response

    except Exception as e:
        return f"Error: {str(e)}"
