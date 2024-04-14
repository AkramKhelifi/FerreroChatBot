import tkinter as tk
from ChatInterface import ChatInterface


if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatInterface(root)
    root.mainloop()
