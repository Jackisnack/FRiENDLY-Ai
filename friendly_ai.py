from langchain_ollama.llms import OllamaLLM
from langchain.memory import ConversationBufferMemory
from melo.api import TTS
from vosk import Model, KaldiRecognizer
import torch
import pyaudio
import nltk
import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font as tkFont
from tkinter import simpledialog
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText
import time
import threading

# Look for vosk model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "vosk-model-small-en-us-0.15")
model = Model(MODEL_PATH)

# Look for nltk_data
nltk_data_path = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_path)

# Initialize the LLM and memory
llm = OllamaLLM(model="openhermes")
memory = ConversationBufferMemory()

RATE = 16000
CHUNK = 1024

listening = True

def listen_and_interpret(gui_instance):
    global listening

    # Set up microphone input
    rec = KaldiRecognizer(model, RATE)
    rec.SetWords(True)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()

    try:
        while listening:
            data = stream.read(CHUNK, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "") # Get recognized text
                if text:
                    gui_instance.root.after(0, gui_instance.send_message, text) # Send the message to the chatbot
            if not listening:
                break
    except Exception as e:
        print(f"Error during auido processing: {e}")
    finally:
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()

# Make sure to use the correct path for the JSON conversation log file
DIR_NAME = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(DIR_NAME, "chat_history.json")

def store_conversation_json(user_message, ai_response):
    conversation_entry = {
        "user": user_message,
        "ai": ai_response
    }

    # Open json file and append conversation entry
    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append(conversation_entry)

    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_past_conversations():
    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    return data

def get_device():
    """Check for GPU availability and return the appropriate device"""
    if torch.cuda.is_available():
        return torch.device("cuda") # Use GPU
    else:
        return torch.device("cpu")

def speak(text):
    # Wait, ensuring message is sent before voice recognition starts
    time.sleep(1)

    device = get_device()
    speed = 0.83
    model = TTS(language="EN", device=device)
    speaker_ids = model.hps.data.spk2id
    output_path = "response.wav"
    model.tts_to_file(text, speaker_ids["EN-BR"], output_path, speed=speed)
    os.system("afplay response.wav")

# Colors
BG_START = "#1E3A8A"  # Dark Blue
BG_END = "#047857"  # Green
BUTTON_COLOR = "#065F46"
HOVER_COLOR = "#04BF8A"
TEXT_COLOR = "#FFFFFF"

# Font
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Exo2-Medium.ttf")

try:
    button_font = tkFont.Font(family=FONT_PATH, size=14)
    root.option_add("*Font", button_font)
except Exception as e:
    print(f"Failed to load font: {e}")
    button_font = ("Ariel", 14)

try:
    text_font = tk.Font.Font(family=FONT_PATH, size=16)
    root.option_add("*Font", text_font)
except Exception as e:
    print(f"Failed to load font: {e}")
    text_font = ("Ariel", 16)

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FRiENDLY-Ai")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Create Gradient Background
        self.canvas = tk.Canvas(self.root, width=500, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.create_gradient()

        # Chat Display
        self.chat_display = ScrolledText(self.root, bg=BG_START, fg=TEXT_COLOR, font=text_font, wrap=tk.WORD, state="disabled")
        self.chat_display.place(x=20, y=20, width=460, height=400)

        # Input Box
        self.input_box = tk.Text(self.root, wrap=tk.WORD, bg="#D1E8E2", fg="#333", font=TEXT_FONT)
        self.input_box.place(x=20, y=440, width=360, height=140)

        # Send Button
        self.send_button = ttk.Button(self.root, text="Send", style="TButton", command=self.send_message)
        self.send_button.place(x=394, y=440, width=86, height=27)

        # Voice Recognition Button ON / OFF
        self.voice_on_button = ttk.Button(self.root, text="🗣️ ON", style="TButton", command=self.start_listening)
        self.voice_on_button.place(x=394, y=478, width=86, height=27)

        self.voice_off_button = ttk.Button(self.root, text="🗣️ OFF", style="TButton", command=self.stop_listening)
        self.voice_off_button.place(x=394, y=515, width=86, height=27)

        # Quit Button
        self.quit_button = ttk.Button(self.root, text="Quit", style="TButton", command=self.quit_program)
        self.quit_button.place(x=394, y=552, width=86, height=27)

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=button_font, background=BUTTON_COLOR, foreground="#000000")
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(background="Hover.TButton"))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(background="TButton"))
        self.style.configure("Hover.TButton", background=HOVER_COLOR, foreground="#000000")

    def create_gradient(self):
        # Create a gradient image
        gradient = Image.new("RGB", (500, 600), color=0)
        for y in range(600):
            r = int(BG_START[1:3], 16) * (1 - y / 600) + int(BG_END[1:3], 16) * (y / 600)
            g = int(BG_START[3:5], 16) * (1 - y / 600) + int(BG_END[3:5], 16) * (y / 600)
            b = int(BG_START[5:7], 16) * (1 - y / 600) + int(BG_END[5:7], 16) * (y / 600)
            for x in range(500):
                gradient.putpixel((x, y), (int(r), int(g), int(b)))
        self.gradient_bg = ImageTk.PhotoImage(gradient)
        self.canvas.create_image(0, 0, image=self.gradient_bg, anchor="nw")

    def get_user_info(self):
        if os.path.getsize(LOG_FILE) == 0:
            # Show pop-up menu to get user information
            username = simpledialog.askstring("Welcome!", "Please enter your name:")
            ai_name = simpledialog.askstring("AI Name", "Please enter your AI's name:")
            if username and ai_name:
                self.save_user_data(username, ai_name)
            else:
                username = "User"
                ai_name = "FRiENDLY-Ai"
                self.save_user_data(username, ai_name)
        else:
            pass # User information already exists
    
    def save_user_data(self, username, ai_name):
        with open(LOG_FILE, "w") as file:
            json.dump({username: f"My name is {username}", ai_name: f"Hello, my name is {ai_name}"}, file)

    def start_listening(self):
        global listening
        listening = True
        threading.Thread(target=listen_and_interpret, args=(self,)).start()
    
    def stop_listening(self):
        global listening
        listening = False # Set to False to stop listening
        self.voice_off_button.config(state="disabled")

    def send_message(self, text=None):
        # Immediately update the GUI
        self.root.update_idletasks()

        user_input = text if text else self.input_box.get("1.0", tk.END).strip()
        if user_input:
            self.root.after(0, self._update_chat_display, user_input)
    
    def _update_chat_display(self, user_input):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{self.username}: {user_input}\n")
        self.chat_display.yview(tk.END)

        self.past_conversations = get_past_conversations()

        self.context = ""
        for entry in self.past_conversations:
            self.context += f"User: {entry['user']}\n{entry['ai']}\n"

        self.context += f"User: {user_input}\n"

        ai_response = llm(self.context)

        self.input_box.delete("1.0", tk.END)
        self.chat_display.insert(tk.END, f"{self.ai_name}: {ai_response}\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state="disabled")

        store_conversation_json(user_input, ai_response)

        speech_thread = threading.Thread(target=speak, args=(ai_response,))
        speech_thread.start()
        
    def quit_program(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()
