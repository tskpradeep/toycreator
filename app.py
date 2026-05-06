import tkinter as tk
from tkinter import messagebox, scrolledtext

class GeminiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Interface")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0e0e0")

        # Global Settings Variables
        self.api_key = tk.StringVar(value="")
        self.model_version = tk.StringVar(value="gemini-1.5-flash")

        self.setup_ui()

    def setup_ui(self):
        # Top Menu / Header Area
        header_frame = tk.Frame(self.root, bg="#e0e0e0")
        header_frame.pack(fill="x", pady=5)

        settings_btn = tk.Button(header_frame, text="⚙ Settings", command=self.open_settings)
        settings_btn.pack(side="right", padx=10)

        # Main Content Area (Split into two windows/panes)
        main_container = tk.PanedWindow(self.root, orient="vertical", bg="#cccccc", sashwidth=4)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Window 1: Prompt Input
        prompt_frame = tk.Frame(main_container, bg="#e0e0e0")
        tk.Label(prompt_frame, text="PROMPT INPUT", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(anchor="w")
        self.prompt_input = scrolledtext.ScrolledText(prompt_frame, height=8, font=("Arial", 11))
        self.prompt_input.pack(fill="both", expand=True, pady=5)
        
        send_btn = tk.Button(prompt_frame, text="Send to AI", command=self.handle_send)
        send_btn.pack(anchor="e", pady=5)
        
        main_container.add(prompt_frame)

        # Window 2: AI Response
        response_frame = tk.Frame(main_container, bg="#e0e0e0")
        tk.Label(response_frame, text="AI RESPONSE", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(anchor="w")
        self.response_output = scrolledtext.ScrolledText(response_frame, state="disabled", font=("Arial", 11), bg="#f5f5f5")
        self.response_output.pack(fill="both", expand=True, pady=5)
        
        main_container.add(response_frame)

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Gemini Configuration")
        settings_win.geometry("400x250")
        settings_win.configure(bg="#e0e0e0")

        tk.Label(settings_win, text="Gemini API Key:", bg="#e0e0e0").pack(pady=(20, 0))
        tk.Entry(settings_win, textvariable=self.api_key, width=40, show="*").pack(pady=5)

        tk.Label(settings_win, text="Model Version:", bg="#e0e0e0").pack(pady=(10, 0))
        tk.OptionMenu(settings_win, self.model_version, "gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro").pack(pady=5)

        save_btn = tk.Button(settings_win, text="Save Settings", command=settings_win.destroy)
        save_btn.pack(pady=20)

    def handle_send(self):
        user_text = self.prompt_input.get("1.0", tk.END).strip()
        if not user_text:
            return

        if not self.api_key.get():
            messagebox.showwarning("Settings Required", "Please enter an API key in Settings.")
            return

        # Placeholder for AI Logic
        self.update_response(f"System: Sending prompt to {self.model_version.get()}...\n(Logic for API call goes here)")

    def update_response(self, text):
        self.response_output.config(state="normal")
        self.response_output.insert(tk.END, text + "\n---\n")
        self.response_output.config(state="disabled")
        self.response_output.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiApp(root)
    root.mainloop()
