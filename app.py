# ai_gui_app.py
import tkinter as tk
from tkinter import messagebox
import requests
import json

# ---------------- SETTINGS ----------------
settings = {
    "url": "https://api.openai.com/v1/chat/completions",
    "apikey": "",
    "model": "gpt-4o-mini"
}

# ---------------- SEND PROMPT ----------------
def send_prompt():
    prompt = input_box.get("1.0", tk.END).strip()

    if not prompt:
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings['apikey']}"
    }

    data = {
        "model": settings["model"],
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            settings["url"],
            headers=headers,
            json=data
        )

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, reply)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- SETTINGS WINDOW ----------------
def open_settings():
    win = tk.Toplevel(root)
    win.title("Settings")
    win.geometry("400x250")

    tk.Label(win, text="API URL").pack()
    url_entry = tk.Entry(win, width=50)
    url_entry.insert(0, settings["url"])
    url_entry.pack()

    tk.Label(win, text="API Key").pack()
    key_entry = tk.Entry(win, width=50, show="*")
    key_entry.insert(0, settings["apikey"])
    key_entry.pack()

    tk.Label(win, text="Model").pack()
    model_entry = tk.Entry(win, width=50)
    model_entry.insert(0, settings["model"])
    model_entry.pack()

    def save():
        settings["url"] = url_entry.get()
        settings["apikey"] = key_entry.get()
        settings["model"] = model_entry.get()
        win.destroy()

    tk.Button(win, text="Save", command=save).pack(pady=10)

# ---------------- MAIN UI ----------------
root = tk.Tk()
root.title("Simple AI Chat")
root.geometry("700x500")

top_frame = tk.Frame(root)
top_frame.pack(fill="x")

tk.Button(top_frame, text="Settings", command=open_settings).pack(
    side="right", padx=5, pady=5
)

tk.Label(root, text="Your Prompt").pack()
input_box = tk.Text(root, height=8)
input_box.pack(fill="x", padx=10)

tk.Button(root, text="Send", command=send_prompt).pack(pady=10)

tk.Label(root, text="AI Reply").pack()
output_box = tk.Text(root, height=12)
output_box.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
