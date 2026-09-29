"""
Start the question-management tool.

    python run_admin.py

Lets the teacher add / edit / delete questions, import them from a CSV file
and see statistics from past games. Talks to the database only through the
repositories - it never touches SQL itself.
"""
import tkinter as tk

from langame.admin.admin_app import AdminApp
from langame.database.db import Database


def main():
    Database().initialize_schema()
    root = tk.Tk()
    root.title("LanGame - Admin")
    root.minsize(800, 560)
    AdminApp(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
