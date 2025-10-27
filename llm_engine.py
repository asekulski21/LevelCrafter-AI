import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_P, TOP_K, DEVICE

class LLMEngine:
    def __init__(self):
        self.device = DEVICE
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.load_model()
    
    def load_model(self):
        print(f"Loading model {MODEL_NAME} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            low_cpu_mem_usage=True
        )
        
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1
        )
        print("Model loaded successfully!")
    
    def generate(self, prompt, max_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE, 
                 top_p=TOP_P, top_k=TOP_K):
        outputs = self.pipeline(
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            do_sample=True,
            return_full_text=False
        )
        
        return outputs[0]['generated_text']
    
    def generate_level(self, prompt):
        response = self.generate(prompt)
        return response

