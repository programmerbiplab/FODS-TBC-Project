# main.py - Sidebar Navigation Version with Tkinter ttk

import tkinter as tk
from tkinter import ttk, messagebox
from user import Admin, Student
from file_handler import read_file
from analytics import get_analytics_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

current_user = None

# ---------- Styling ----------
PRIMARY_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
BG_COLOR = "#ecf0f1"
FONT_NAME = "Segoe UI"

class SidebarButton(ttk.Button):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, command=command)
        self.configure(style="Sidebar.TButton")

class LoginFrame(ttk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.configure(style="Login.TFrame")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Student Profile System Login", style="Title.TLabel").pack(pady=40)

        form_frame = ttk.Frame(self, style="Login.TFrame")
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Username:", style="Label.TLabel").grid(row=0, column=0, sticky=tk.E, pady=10, padx=10)
        self.username_entry = ttk.Entry(form_frame, width=30, font=(FONT_NAME, 12))
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(form_frame, text="Password:", style="Label.TLabel").grid(row=1, column=0, sticky=tk.E, pady=10, padx=10)
        self.password_entry = ttk.Entry(form_frame, show="*", width=30, font=(FONT_NAME, 12))
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        login_btn = ttk.Button(self, text="Login", command=self.attempt_login, style="Accent.TButton")
        login_btn.pack(pady=30)

    def attempt_login(self):
        uid = self.username_entry.get()
        pwd = self.password_entry.get()
        credentials = read_file("passwords.txt")
        users = read_file("users.txt")

        for cred in credentials:
            u, p = cred.strip().split(",")
            if uid == u and pwd == p:
                for user in users:
                    parts = user.strip().split(",")
                    if parts[0] == uid:
                        role = parts[2]
                        name = parts[1]
                        self.on_login_success(uid, name, role)
                        return
        messagebox.showerror("Login Failed", "Invalid username or password.")


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Profile Management System")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.current_user = None
        self.frames = {}

        # Setup styles
        self.setup_styles()

        # Start with login screen
        self.login_frame = LoginFrame(self, self.login_success)
        self.login_frame.pack(fill="both", expand=True)

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure("TFrame", background=BG_COLOR)
        style.configure("Login.TFrame", background=BG_COLOR)
        style.configure("Title.TLabel", font=(FONT_NAME, 24, "bold"), background=BG_COLOR, foreground=PRIMARY_COLOR)
        style.configure("Label.TLabel", font=(FONT_NAME, 14), background=BG_COLOR, foreground=PRIMARY_COLOR)
        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground="white", font=(FONT_NAME, 14))
        style.map("Accent.TButton", background=[('active', '#2980b9')])
        style.configure("Sidebar.TButton", font=(FONT_NAME, 14), background=PRIMARY_COLOR, foreground="white", padding=10)
        style.map("Sidebar.TButton", background=[('active', '#34495e')])

        style.configure("Header.TLabel", font=(FONT_NAME, 18, "bold"), background=BG_COLOR, foreground=PRIMARY_COLOR)

    def login_success(self, uid, name, role):
        self.current_user = Admin(uid, name, role) if role == "admin" else Student(uid, name, role)
        self.login_frame.destroy()
        self.build_main_ui(role)

    def build_main_ui(self, role):
        # Main container frames
        self.sidebar = ttk.Frame(self, width=200, style="TFrame")
        self.sidebar.pack(side="left", fill="y")

        self.content = ttk.Frame(self, style="TFrame")
        self.content.pack(side="right", fill="both", expand=True)

        # Sidebar Buttons depending on role
        buttons = []
        if role == "admin":
            buttons = [
                ("Dashboard", self.show_dashboard),
                ("Add User", self.show_add_user),
                ("Delete User", self.show_delete_user),
                ("Update Info", self.show_update_info),
                ("Analytics", self.show_analytics),
                ("Logout", self.logout)
            ]
        else:
            buttons = [
                ("Profile", self.show_profile),
                ("Grades", self.show_grades),
                ("ECA", self.show_eca),
                ("Update Profile", self.show_update_profile),
                ("Logout", self.logout)
            ]

        for (text, command) in buttons:
            btn = SidebarButton(self.sidebar, text=text, command=command)
            btn.pack(fill="x", pady=5, padx=10)

        # Create frames for content pages
        if role == "admin":
            self.frames['dashboard'] = AdminDashboardFrame(self.content, self.current_user)
            self.frames['add_user'] = AdminAddUserFrame(self.content, self.current_user)
            self.frames['delete_user'] = AdminDeleteUserFrame(self.content, self.current_user)
            self.frames['update_info'] = AdminUpdateInfoFrame(self.content, self.current_user)
            self.frames['analytics'] = AdminAnalyticsFrame(self.content)
        else:
            self.frames['profile'] = StudentProfileFrame(self.content, self.current_user)
            self.frames['grades'] = StudentGradesFrame(self.content, self.current_user)
            self.frames['eca'] = StudentECAFrame(self.content, self.current_user)
            self.frames['update_profile'] = StudentUpdateProfileFrame(self.content, self.current_user)

        # Place all frames in the same location
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Show default page
        self.show_first_page(role)

    def show_first_page(self, role):
        if role == "admin":
            self.show_dashboard()
        else:
            self.show_profile()

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def show_dashboard(self):
        self.show_frame('dashboard')

    def show_add_user(self):
        self.show_frame('add_user')

    def show_delete_user(self):
        self.show_frame('delete_user')

    def show_update_info(self):
        self.show_frame('update_info')

    def show_analytics(self):
        self.show_frame('analytics')

    def show_profile(self):
        self.show_frame('profile')

    def show_grades(self):
        self.show_frame('grades')

    def show_eca(self):
        self.show_frame('eca')

    def show_update_profile(self):
        self.show_frame('update_profile')

    def logout(self):
        for frame in self.frames.values():
            frame.destroy()
        self.sidebar.destroy()
        self.content.destroy()
        self.current_user = None
        self.frames = {}
        self.login_frame = LoginFrame(self, self.login_success)
        self.login_frame.pack(fill="both", expand=True)

# --------------------------
# Admin frames below

class AdminDashboardFrame(ttk.Frame):
    def __init__(self, master, admin):
        super().__init__(master)
        self.admin = admin
        ttk.Label(self, text="Admin Dashboard", style="Header.TLabel").pack(pady=20)
        # Add more dashboard info here if you want
        ttk.Label(self, text="Welcome, Admin " + self.admin.name, font=(FONT_NAME, 14)).pack(pady=10)

class AdminAddUserFrame(ttk.Frame):
    def __init__(self, master, admin):
        super().__init__(master)
        self.admin = admin
        ttk.Label(self, text="Add New User", style="Header.TLabel").pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="User ID:").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.uid_entry = ttk.Entry(form, width=30)
        self.uid_entry.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(form, text="Name:").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(form, text="Role:").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.role_combo = ttk.Combobox(form, values=["student", "admin"], state="readonly", width=27)
        self.role_combo.grid(row=2, column=1, padx=10, pady=8)
        self.role_combo.current(0)

        ttk.Label(form, text="Password:").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.pwd_entry = ttk.Entry(form, show="*", width=30)
        self.pwd_entry.grid(row=3, column=1, padx=10, pady=8)

        ttk.Button(self, text="Add User", command=self.add_user, style="Accent.TButton").pack(pady=15)

    def add_user(self):
        uid = self.uid_entry.get().strip()
        name = self.name_entry.get().strip()
        role = self.role_combo.get()
        pwd = self.pwd_entry.get().strip()

        if not (uid and name and pwd):
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            self.admin.add_user(uid, name, role, pwd)
            messagebox.showinfo("Success", f"User '{uid}' added.")
            self.uid_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.pwd_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AdminDeleteUserFrame(ttk.Frame):
    def __init__(self, master, admin):
        super().__init__(master)
        self.admin = admin
        ttk.Label(self, text="Delete User", style="Header.TLabel").pack(pady=20)

        self.uid_entry = ttk.Entry(self, width=30)
        self.uid_entry.pack(pady=15)
        self.uid_entry.insert(0, "Enter User ID to delete")

        ttk.Button(self, text="Delete User", command=self.delete_user, style="Accent.TButton").pack(pady=10)

    def delete_user(self):
        uid = self.uid_entry.get().strip()
        if not uid:
            messagebox.showerror("Error", "Please enter User ID")
            return
        if uid == self.admin.user_id:
            messagebox.showwarning("Warning", "You cannot delete yourself!")
            return
        self.admin.delete_user(uid)
        messagebox.showinfo("Deleted", f"User '{uid}' deleted.")
        self.uid_entry.delete(0, tk.END)


class AdminUpdateInfoFrame(ttk.Frame):
    def __init__(self, master, admin):
        super().__init__(master)
        self.admin = admin
        ttk.Label(self, text="Update Student Grades and ECA", style="Header.TLabel").pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Student ID:").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self.sid_entry = ttk.Entry(form, width=30)
        self.sid_entry.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(form, text="Grades (5 comma-separated):").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.grades_entry = ttk.Entry(form, width=30)
        self.grades_entry.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(form, text="ECA Activities (comma-separated):").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.eca_entry = ttk.Entry(form, width=30)
        self.eca_entry.grid(row=2, column=1, padx=10, pady=8)

        ttk.Button(self, text="Update Info", command=self.update_info, style="Accent.TButton").pack(pady=15)

    def update_info(self):
        uid = self.sid_entry.get().strip()
        grades_str = self.grades_entry.get().strip()
        eca_str = self.eca_entry.get().strip()

        if not uid:
            messagebox.showerror("Error", "Please enter Student ID")
            return

        if grades_str:
            try:
                grades = list(map(int, grades_str.split(",")))
                if len(grades) != 5:
                    raise ValueError
                self.admin.update_grades(uid, grades)
            except:
                messagebox.showerror("Error", "Enter 5 valid integer grades separated by commas")
                return

        if eca_str:
            activities = [x.strip() for x in eca_str.split(",") if x.strip()]
            self.admin.update_eca(uid, activities)

        messagebox.showinfo("Success", "Student info updated.")


class AdminAnalyticsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Analytics Dashboard", style="Header.TLabel").pack(pady=20)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.tight_layout(pad=4)

        avg_grades, eca_counts, averages, student_ids = get_analytics_data()

        subjects = ["Math", "Science", "English", "Social", "Computer"]
        ax1.bar(subjects, avg_grades, color=ACCENT_COLOR)
        ax1.set_title("Average Grades per Subject")
        ax1.set_ylim(0, 100)
        ax1.set_ylabel("Marks")

        ax2.scatter(eca_counts, averages, c="#e74c3c", alpha=0.7)
        ax2.set_title("ECA Activities vs Academic Performance")
        ax2.set_xlabel("Number of ECAs")
        ax2.set_ylabel("Average Grade")
        ax2.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        alert_text = tk.Text(self, height=7, width=85, font=(FONT_NAME, 11))
        alert_text.pack(pady=15)
        alert_text.insert(tk.END, "Performance Alerts:\n")
        alert_text.insert(tk.END, "Students with average grades below 40:\n")

        low_perf = [(sid, avg) for sid, avg in zip(student_ids, averages) if avg < 40]
        if low_perf:
            for sid, avg in low_perf:
                alert_text.insert(tk.END, f" - {sid}: {avg:.2f}\n")
        else:
            alert_text.insert(tk.END, " None - All students performing well!\n")

        alert_text.config(state="disabled")


# --------- Student frames -----------

class StudentProfileFrame(ttk.Frame):
    def __init__(self, master, student):
        super().__init__(master)
        self.student = student
        ttk.Label(self, text="Your Profile", style="Header.TLabel").pack(pady=20)

        self.text = tk.Text(self, height=10, width=60, font=(FONT_NAME, 12), state="disabled")
        self.text.pack(pady=10)
        self.load_profile()

    def load_profile(self):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        info = f"User ID: {self.student.user_id}\nName: {self.student.name}\nRole: Student"
        self.text.insert(tk.END, info)
        self.text.config(state="disabled")

class StudentGradesFrame(ttk.Frame):
    def __init__(self, master, student):
        super().__init__(master)
        self.student = student
        ttk.Label(self, text="Your Grades", style="Header.TLabel").pack(pady=20)

        grades = self.student.view_grades()
        subjects = ["Math", "Science", "English", "Social", "Computer"]
        text = ""
        if grades:
            for s, g in zip(subjects, grades):
                text += f"{s}: {g}\n"
        else:
            text = "No grades available."

        ttk.Label(self, text=text, font=(FONT_NAME, 13)).pack(pady=10)

class StudentECAFrame(ttk.Frame):
    def __init__(self, master, student):
        super().__init__(master)
        self.student = student
        ttk.Label(self, text="Your Extracurricular Activities", style="Header.TLabel").pack(pady=20)

        eca = self.student.view_eca()
        text = ", ".join(eca) if eca else "No ECA data available."
        ttk.Label(self, text=text, font=(FONT_NAME, 13)).pack(pady=10)

class StudentUpdateProfileFrame(ttk.Frame):
    def __init__(self, master, student):
        super().__init__(master)
        self.student = student
        ttk.Label(self, text="Update Your Name", style="Header.TLabel").pack(pady=20)

        self.name_entry = ttk.Entry(self, width=40, font=(FONT_NAME, 13))
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, self.student.name)

        ttk.Button(self, text="Update Name", command=self.update_name, style="Accent.TButton").pack(pady=10)

    def update_name(self):
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        self.student.update_profile(new_name)
        messagebox.showinfo("Success", "Name updated.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
