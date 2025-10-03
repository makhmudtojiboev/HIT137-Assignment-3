# gui_components.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading, webbrowser
import ttkbootstrap as tb
from oop_demo import GenericModel
from hf_models import HFModelWrapper
from utils import choose_image_file, show_error
from PIL import Image, ImageTk
import os

class ModernApp(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("AI Toolkit - Tkinter HuggingFace App")
        self.geometry("1200x800")
        
        # Data storage for image output
        self.tk_image = None 
        self.output_image_label = None

        # Models
        self.hf = HFModelWrapper()
        self.generic_model = GenericModel("Generic", self.hf)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_run_tab()
        self._create_oop_tab()
        self._create_model_info_tab()
        self._create_about_tab()

        # Status bar
        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w", relief="sunken").pack(side=tk.BOTTOM, fill=tk.X)

    # ----------- Run Models -----------
    def _create_run_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Run Models")

        # Dropdown
        frame_top = ttk.Frame(tab, padding=10)
        frame_top.pack(fill=tk.X)

        ttk.Label(frame_top, text="Select Task:").grid(row=0, column=0, sticky="w")
        self.task_combo = ttk.Combobox(frame_top, values=[
            "Text Generation", "Image Classification"
        ], width=30, state="readonly")
        self.task_combo.current(0)
        self.task_combo.grid(row=0, column=1, padx=5)

        # Input
        input_frame = ttk.LabelFrame(tab, text="Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.text_input = scrolledtext.ScrolledText(input_frame, height=5)
        self.text_input.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(input_frame, text="Choose Image", command=lambda: self._select_file("image"), bootstyle="secondary").pack(side=tk.LEFT, padx=5)

        # Run
        run_frame = ttk.Frame(tab, padding=10)
        run_frame.pack(fill=tk.X)

        self.run_btn = ttk.Button(run_frame, text="▶ Run", command=self._start_model_thread, bootstyle="success")
        self.run_btn.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(run_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, padx=10, expand=True)

        # Output
        output_frame = ttk.LabelFrame(tab, text="Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_text = scrolledtext.ScrolledText(output_frame, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.output_image_label = ttk.Label(output_frame, text="Generated Image Preview", background='white')

    def _select_file(self, ftype):
        path = choose_image_file()
        if path:
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, path)

    def _start_model_thread(self):
        self.run_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status.set("Running inference...")
        
        self.output_image_label.pack_forget()
        
        threading.Thread(target=self.run_model, daemon=True).start()

    def run_model(self):
        task = self.task_combo.get()
        raw_input = self.text_input.get("1.0", tk.END).strip()
        
        if not raw_input:
            self.after(0, lambda: show_error("Please provide input."))
            self._cleanup_thread()
            return
            
        try:
            if task == "Text Generation":
                result = self.generic_model.run_text_generation(raw_input)
            elif task == "Image Classification":
                if not os.path.isfile(raw_input):
                    raise FileNotFoundError(f"Image file not found: {raw_input}")
                result = self.generic_model.run_image(raw_input)
            else:
                result = {"output": "Unsupported task selected."}

            self.after(0, lambda: self._update_output_display(result["output"], task))

        except FileNotFoundError as e:
            self.after(0, lambda err=e: show_error(f"File Error: {err}"))
        except Exception as e:
            self.after(0, lambda err=e: show_error(f"Inference Error: {err}"))
        finally:
            self._cleanup_thread()

    def _cleanup_thread(self):
        self.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
        self.after(0, lambda: self.progress.stop())
        self.after(0, lambda: self.status.set("Ready"))
        
    def _update_output_display(self, result_data, task):
        self.output_text.delete("1.0", tk.END)
        
        output_str = str(result_data)
        if task == "Image Classification" and isinstance(result_data, list):
            output_str = f"--- Image Classification Results ---\n"
            for i, item in enumerate(result_data):
                output_str += f"{i+1}. {item['label']} (Confidence: {item['score']:.4f})\n"

        self.output_text.insert(tk.END, output_str)

    # ----------- OOP Concepts -----------
    def _create_oop_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="OOP Concepts")

        text = (
            "OOP Concepts Demonstrated in this Project:\n\n"
            "🔹 **Multiple Inheritance** → `GenericModel` inherits from `BaseModelConfig`, `TextHandler`, and `ImageHandler`.\n\n"
            "🔹 **Decorators** → The `@timed` decorator is used on all `GenericModel.run_X` methods to measure execution time.\n\n"
            "🔹 **Encapsulation** → `BaseModelConfig` manages internal state using a **private attribute** (`__version`) and a **protected attribute** (`_model_name`).\n\n"
            "🔹 **Polymorphism** → The GUI calls specific methods (`run_text_generation`, `run_image`) with common structure but different logic.\n\n"
            "🔹 **Method Overriding** → The abstract method `BaseModelConfig.run()` is overridden in `GenericModel`.\n"
        )

        box = scrolledtext.ScrolledText(tab, wrap="word")
        box.insert(tk.END, text)
        box.configure(state="disabled")
        box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ----------- Model Info -----------
    def _create_model_info_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Model Info")

        text = (
            "📌 Implemented Hugging Face Models:\n\n"
            "1. **Text Generation**:\n"
            "   - **Model:** `distilgpt2` (Distilled GPT-2)\n"
            "   - **Category:** Text Generation\n"
            "   - **Input:** Text prompt\n"
            "   - **Output:** Generated text continuation\n"
            "   - **Size:** ~350MB (Lightweight)\n\n"
            "2. **Image Classification**:\n"
            "   - **Model:** `google/mobilenet_v2_1.0_224`\n"
            "   - **Category:** Image Analysis\n"
            "   - **Input:** Image file path\n"
            "   - **Output:** Classification labels with confidence scores\n"
            "   - **Size:** ~15MB (Very lightweight)\n\n"
            "✅ Total size: ~365MB (Follows 'not larger in size' requirement)\n"
            "✅ Two different categories\n"
            "✅ No massive downloads\n"
        )

        box = scrolledtext.ScrolledText(tab, wrap="word")
        box.insert(tk.END, text)
        box.configure(state="disabled")
        box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ----------- About -----------
    def _create_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="About")

        ttk.Label(tab, text="HIT137 - Group Assignment 3", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(tab, text="Developed by: Your Group Names").pack(pady=5)

        link = ttk.Label(tab, text="GitHub Repository", foreground="blue", cursor="hand2")
        link.pack(pady=10)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/makhmudtojiboev/Assignment-3-Software-Now-"))