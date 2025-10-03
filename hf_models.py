# hf_models.py
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import os

class HFModelWrapper:
    """
    A wrapper for Hugging Face pipelines using lightweight models.
    """
    def __init__(self):
        print("Initializing lightweight models...")
        
        # 1. Image Classification (Lightweight)
        print("Loading image classification model...")
        self.img_classifier = pipeline(
            "image-classification",
            model="google/mobilenet_v2_1.0_224",
            device=-1
        )
        
        # 2. Text Generation (Lightweight)
        print("Loading text generation model...")
        self.text_generator = pipeline(
            "text-generation",
            model="distilgpt2",  # Smaller version of GPT-2 (~350MB)
            device=-1
        )
        
        print("✓ All models loaded successfully")

    def generate_text(self, prompt: str) -> str:
        """Generate text based on prompt."""
        try:
            result = self.text_generator(
                prompt,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
            
            generated_text = result[0]['generated_text']
            return f"🤖 GENERATED TEXT:\n{generated_text}"
            
        except Exception as e:
            return f"Error in text generation: {str(e)}"

    def classify_image(self, image_path: str) -> list:
        """Classify an image into categories."""
        if not os.path.exists(image_path):
            return [{"label": "Error", "score": 0.0, "message": f"File not found: {os.path.basename(image_path)}"}]

        try:
            result = self.img_classifier(image_path)
            return result
        except Exception as e:
            return [{"label": "Error", "score": 0.0, "message": f"Classification failed: {str(e)}"}]