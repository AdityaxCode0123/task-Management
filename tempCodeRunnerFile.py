
# Beautiful Task Management Software

import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
from pathlib import Path

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.tasks_file = Path('tasks.json')
        self.setup_ui()
        self.load_tasks()
        
    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title("✨ Beautiful Task Manager")
        self.window.geometry("600x700")
        self.window.configure(bg='#f0f2f5')
        self.window.resizable(True, True)
        
        # Configure styles
        self.setup_styles()
        
        # Header
        header_frame = tk.Frame(self.window, bg='#4a90e2', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📋 Task Manager", 
                              font=('Segoe UI', 24, 'bold'), 
                              fg='white', bg='#4a90e2')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="Organize your tasks beautifully", 
                                 font=('Segoe UI', 11), 
                                 fg='#e8f4fd', bg='#4a90e2')
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.window, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        # Input section
        input_card = tk.Frame(main_frame, bg='white', relief='flat', bd=0)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        # Add shadow effect
        shadow_frame = tk.Frame(main_frame, bg='#e0e0e0', height=2)
        shadow_frame.pack(fill=tk.X, pady=(0, 18))
        
        input_inner = tk.Frame(input_card, bg='white')
        input_inner.pack(fill=tk.X, padx=25, pady=25)
        
        # Task input
        tk.Label(input_inner, text="📝 Task Description", 
                font=('Segoe UI', 12, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 8))
        
        self.task_entry = tk.Entry(input_inner, font=('Segoe UI', 11), 
                                  relief='flat', bd=0, bg='#f8f9fa',
                                  highlightthickness=2, highlightcolor='#4a90e2',
                                  highlightbackground='#e9ecef')
        self.task_entry.pack(fill=tk.X, ipady=12, pady=(0, 20))
        
        # Due date input
        tk.Label(input_inner, text="📅 Due Date (YYYY-MM-DD)", 
                font=('Segoe UI', 12, 'bold'), 
                fg='#2c3e50', bg='white').pack(anchor='w', pady=(0, 8))
        
        self.date_entry = tk.Entry(input_inner, font=('Segoe UI', 11), 
                                  relief='flat', bd=0, bg='#f8f9fa',
                                  highlightthickness=2, highlightcolor='#4a90e2',
                                  highlightbackground='#e9ecef')
        self.date_entry.pack(fill=tk.X, ipady=12, pady=(0, 25))
        
        # Buttons
        button_frame = tk.Frame(input_inner, bg='white')
        button_frame.pack(fill=tk.X)
        
        self.add_btn = tk.Button(button_frame, text="➕ Add Task", 
                                command=self.add_task,
                                font=('Segoe UI', 11, 'bold'),
                                bg='#27ae60', fg='white', 
                                relief='flat', bd=0,
                                padx=25, pady=12,
                                cursor='hand2',
                                activebackground='#229954')
        self.add_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.delete_btn = tk.Button(button_frame, text="🗑️ Delete Selected", 
                                   command=self.delete_task,
                                   font=('Segoe UI', 11, 'bold'),
                                   bg='#e74c3c', fg='white', 
                                   relief='flat', bd=0,
                                   padx=25, pady=12,
                                   cursor='hand2',
                                   activebackground='#c0392b')
        self.delete_btn.pack(side=tk.LEFT)
        
        # Task list section
        list_card = tk.Frame(main_frame, bg='white', relief='flat', bd=0)
        list_card.pack(fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Frame(list_card, bg='white')
        list_header.pack(fill=tk.X, padx=25, pady=(25, 15))
        
        tk.Label(list_header, text="📋 Your Tasks", 
                font=('Segoe UI', 14, 'bold'), 
                fg='#2c3e50', bg='white').pack(side=tk.LEFT)
        
        self.task_count = tk.Label(list_header, text="0 tasks", 
                                  font=('Segoe UI', 10), 
                                  fg='#7f8c8d', bg='white')
        self.task_count.pack(side=tk.RIGHT)
        
        # Task list with scrollbar
        list_frame = tk.Frame(list_card, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        self.task_listbox = tk.Listbox(list_frame, 
                                      font=('Segoe UI', 11),
                                      relief='flat', bd=0,
                                      bg='#f8f9fa',
                                      selectbackground='#4a90e2',
                                      selectforeground='white',
                                      highlightthickness=0,
                                      activestyle='none')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.task_listbox.yview)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Status bar
        status_frame = tk.Frame(self.window, bg='#34495e', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    font=('Segoe UI', 9), 
                                    fg='white', bg='#34495e')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Bind events
        self.window.bind('<Return>', lambda e: self.add_task())
        self.task_entry.bind('<FocusIn>', self.on_entry_focus)
        self.date_entry.bind('<FocusIn>', self.on_entry_focus)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
    def on_entry_focus(self, event):
        event.widget.configure(highlightbackground='#4a90e2')
        
    def update_task_count(self):
        count = len(self.tasks)
        self.task_count.config(text=f"{count} task{'s' if count != 1 else ''}")
        
    def set_status(self, message, color='white'):
        self.status_label.config(text=message, fg=color)
        self.window.after(3000, lambda: self.status_label.config(text="Ready", fg='white'))
        
    def add_task(self):
        task = self.task_entry.get().strip()
        due_date = self.date_entry.get().strip()
        
        if not task or not due_date:
            self.set_status("⚠️ Please enter both task and due date!", '#e74c3c')
            return
            
        try:
            parsed_date = datetime.strptime(due_date, '%Y-%m-%d')
            task_data = {'task': task, 'due_date': due_date, 'created': datetime.now().isoformat()}
            self.tasks.append(task_data)
            
            # Check if task is overdue
            today = datetime.now().date()
            task_date = parsed_date.date()
            
            if task_date < today:
                status_icon = "🔴"
            elif task_date == today:
                status_icon = "🟡"
            else:
                status_icon = "🟢"
                
            display_text = f"{status_icon} {task} (Due: {due_date})"
            self.task_listbox.insert(tk.END, display_text)
            
            self.clear_entries()
            self.save_tasks()
            self.update_task_count()
            self.set_status(f"✅ Task '{task}' added successfully!", '#27ae60')
        except ValueError:
            self.set_status("❌ Invalid date format! Use YYYY-MM-DD", '#e74c3c')
    
    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.task_entry.focus()
            
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            self.set_status("⚠️ Please select a task to delete!", '#e74c3c')
            return
            
        try:
            index = selection[0]
            task_name = self.tasks[index]['task']
            self.task_listbox.delete(index)
            self.tasks.pop(index)
            self.save_tasks()
            self.update_task_count()
            self.set_status(f"🗑️ Task '{task_name}' deleted!", '#e74c3c')
        except IndexError:
            self.set_status("❌ Failed to delete task!", '#e74c3c')
            
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w') as file:
                json.dump(self.tasks, file, indent=2)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
            
    def load_tasks(self):
        if not self.tasks_file.exists():
            self.update_task_count()
            return
            
        try:
            with open(self.tasks_file, 'r') as file:
                self.tasks = json.load(file)
                
            today = datetime.now().date()
            for task_data in self.tasks:
                if isinstance(task_data, dict):
                    task_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()
                    
                    if task_date < today:
                        status_icon = "🔴"
                    elif task_date == today:
                        status_icon = "🟡"
                    else:
                        status_icon = "🟢"
                        
                    display_text = f"{status_icon} {task_data['task']} (Due: {task_data['due_date']})"
                else:
                    display_text = task_data
                self.task_listbox.insert(tk.END, display_text)
            
            self.update_task_count()
            self.set_status(f"📂 Loaded {len(self.tasks)} tasks", '#27ae60')
        except (json.JSONDecodeError, IOError) as e:
            self.set_status(f"❌ Failed to load tasks: {e}", '#e74c3c')
            self.tasks = []
            self.update_task_count()
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TaskManager()
    app.run()