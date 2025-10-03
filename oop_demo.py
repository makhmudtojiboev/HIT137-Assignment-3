# oop_demo.py
import time
from abc import ABC, abstractmethod
 
# ---------------- Decorator ----------------
def timed(func):
    """Decorator to measure execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} executed in {end - start:.2f}s")
        return result
    return wrapper
 
# ---------------- Base Classes (Encapsulation and Abstraction) ----------------
class BaseModelConfig(ABC):
    """Base class demonstrating encapsulation and abstraction."""
    def __init__(self, model_name):
        self._model_name = model_name    # Protected attribute
        self.__version = "1.0"           # Private attribute
 
    def get_version(self):
        """Getter for private attribute (Encapsulation)."""
        return self.__version
 
    @abstractmethod
    def run(self, data):
        """Abstract method for Polymorphism."""
        pass
 
# Handlers for Multiple Inheritance
class TextHandler:
    """Mixin for text-based preprocessing."""
    def preprocess_text(self, text):
        return text.strip()
 
class ImageHandler:
    """Mixin for image-based preprocessing."""
    def preprocess_image(self, path):
        return path
 
# ---------------- Generic Model (Multiple Inheritance) ----------------
class GenericModel(BaseModelConfig, TextHandler, ImageHandler):
    """
    Concrete model class demonstrating Multiple Inheritance.
    """
    def __init__(self, model_name, hf_wrapper):
        super().__init__(model_name)
        self.hf = hf_wrapper
 
    # Method Overriding
    @timed
    def run(self, data):
        return {"output": "Error: Specific task handler not called"}
 
    # Text Generation
    @timed
    def run_text_generation(self, prompt):
        clean = self.preprocess_text(prompt)
        return {"output": self.hf.generate_text(clean)}
 
    # Image Classification
    @timed
    def run_image(self, path):
        clean = self.preprocess_image(path)
        return {"output": self.hf.classify_image(clean)}