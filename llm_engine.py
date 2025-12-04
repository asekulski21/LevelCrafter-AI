# LLM Engine - loads and runs the TinyLlama model

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from config import MODEL_NAME, DEVICE, MAX_TOKENS, TEMPERATURE

class LLMEngine:
    """Handles loading the model and generating text."""
    
    def __init__(self):
        print(f"Loading {MODEL_NAME} on {DEVICE}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        if DEVICE == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        else:
            self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
            self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=-1)
        
        print("Model loaded.")
    
    def generate(self, prompt):
        """Generate text from a prompt."""
        output = self.pipe(
            prompt,
            max_new_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True,
            return_full_text=False
        )
        return output[0]['generated_text']
