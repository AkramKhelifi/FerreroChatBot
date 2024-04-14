import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkFont
from FerreroChatbot import FerreroChatbot
from utilities import preprocess_input

class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("Ferrero Chatbot")
        master.geometry("1000x600")

        customFont = tkFont.Font(family="Helvetica", size=14)

        self.chatbox = scrolledtext.ScrolledText(master, state='disabled', height=20, width=70, wrap='word', font=customFont)
        self.chatbox.tag_configure('user', foreground='blue')
        self.chatbox.tag_configure('bot', foreground='red')
        self.chatbox.tag_configure('normal', foreground='black')
        self.chatbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_box = tk.Entry(master, width=60, font=customFont)
        self.message_box.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send, height=2, width=20, font=customFont)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.chatbot = FerreroChatbot()
        self.initiate_start()

    def send(self):
        user_input = self.message_box.get()
        self.message_box.delete(0, tk.END)
        self.update_chatbox("You: ", "user")
        self.update_chatbox(user_input + "\n", "normal")

        response = self.chatbot.respond(preprocess_input(user_input))
        if response:
            self.update_chatbox("Bot: ", "bot")
            self.update_chatbox(response + "\n", "normal")
        else:
            self.update_chatbox("Bot: Sorry, I didn't understand that.\n", "normal")

    def update_chatbox(self, message, tag):
        self.chatbox.config(state='normal')
        self.chatbox.insert(tk.END, message, tag)
        self.chatbox.config(state='disabled')
        self.chatbox.yview(tk.END)

    def initiate_start(self):
        welcome_text = self.chatbot.welcome_message()
        self.update_chatbox("Bot: ", "bot")
        self.update_chatbox(welcome_text + "\n", "normal")
