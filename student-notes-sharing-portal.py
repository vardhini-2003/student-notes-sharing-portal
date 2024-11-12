import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

class Note:
    def _init_(self, title, content, author, tags=None, sharing_type="public", shared_with=None):
        self.title = title
        self.content = content
        self.author = author
        self.tags = tags if tags else []
        self.sharing_type = sharing_type
        self.shared_with = shared_with

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "tags": self.tags,
            "sharing_type": self.sharing_type,
            "shared_with": self.shared_with
        }

users = {
    "admin": "password123",
    "user1": "pass1",
}

notes = []

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_users():
    global users
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)

def save_notes():
    with open("notes.json", "w") as f:
        json.dump([note.to_dict() for note in notes], f)

def load_notes():
    global notes
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as f:
            notes.extend([Note(**note_data) for note_data in json.load(f)])

def register():
    username = simpledialog.askstring("Register", "Enter a new username:")
    if username in users:
        messagebox.showerror("Error", "Username already exists.")
        return None
    password = simpledialog.askstring("Register", "Enter a new password:", show="*")
    users[username] = password
    save_users()
    messagebox.showinfo("Success", "Registration successful!")
    return username

def login():
    username = simpledialog.askstring("Login", "Enter your username:")
    password = simpledialog.askstring("Login", "Enter your password:", show="*")
    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        return username
    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        return None

def browse_file():
    file_path = filedialog.askopenfilename(title="Select file to upload")
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        return os.path.basename(file_path), content
    else:
        return None, None

def upload_note():
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return
    title = simpledialog.askstring("Upload Note", "Enter note title:")
    file_name, content = browse_file()
    if not content:
        return
    tags = simpledialog.askstring("Tags", "Enter up to three tags, separated by commas:")
    tags = [tag.strip() for tag in tags.split(",")[:3]]
    sharing_type = simpledialog.askstring("Sharing", "Enter sharing type (public/private):").lower()
    shared_with = None
    if sharing_type == "private":
        shared_with = simpledialog.askstring("Private Share", "Enter username to share with:")
        if shared_with not in users:
            messagebox.showerror("Error", "User does not exist. Defaulting to public sharing.")
            sharing_type = "public"
            shared_with = None
    note = Note(title, content, current_user, tags, sharing_type, shared_with)
    notes.append(note)
    messagebox.showinfo("Success", "Note uploaded successfully!")

def view_notes():
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return
    accessible_notes = [
        note for note in notes
        if note.sharing_type == "public" or note.author == current_user or note.shared_with == current_user
    ]
    if accessible_notes:
        notes_text = ""
        for note in accessible_notes:
            notes_text += f"Title: {note.title}\nAuthor: {note.author}\nTags: {', '.join(note.tags)}\n"
            notes_text += f"Sharing: {note.sharing_type}\nContent:\n{note.content}\n\n"
        messagebox.showinfo("View Notes", notes_text)
    else:
        messagebox.showinfo("View Notes", "No notes available.")

def search_notes_by_tag():
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return
    search_tag = simpledialog.askstring("Search Notes", "Enter tag to search:")
    found_notes = [
        note for note in notes
        if search_tag in note.tags and (note.sharing_type == "public" or note.author == current_user or note.shared_with == current_user)
    ]
    if found_notes:
        notes_text = ""
        for note in found_notes:
            notes_text += f"Title: {note.title}\nAuthor: {note.author}\nTags: {', '.join(note.tags)}\n"
            notes_text += f"Sharing: {note.sharing_type}\nContent:\n{note.content}\n\n"
        messagebox.showinfo("Search Results", notes_text)
    else:
        messagebox.showinfo("Search Results", f"No accessible notes found with tag '{search_tag}'.")

def logout():
    global current_user
    current_user = None
    save_notes()
    messagebox.showinfo("Logout", "You have logged out and notes have been saved.")

def main_menu():
    global current_user
    root = tk.Tk()
    root.title("Collaborative Knowledge Repository")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    # Style Configuration
    style = ttk.Style(root)
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    # Frame for Buttons
    frame = ttk.Frame(root, padding="20 20 20 20", relief="ridge")
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Buttons
    ttk.Button(frame, text="Register", command=register, width=30).grid(row=0, column=0, pady=5)
    ttk.Button(frame, text="Login", command=lambda: setattr("current_user", login()), width=30).grid(row=1, column=0, pady=5)
    ttk.Button(frame, text="Upload Note", command=upload_note, width=30).grid(row=2, column=0, pady=5)
    ttk.Button(frame, text="View Notes", command=view_notes, width=30).grid(row=3, column=0, pady=5)
    ttk.Button(frame, text="Search Notes by Tag", command=search_notes_by_tag, width=30).grid(row=4, column=0, pady=5)
    ttk.Button(frame, text="Logout", command=logout, width=30).grid(row=5, column=0, pady=5)

    root.mainloop()

if _name_ == "_main_":
    load_users()
    load_notes()
    current_user = None
    main_menu()
