import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import csv
import os
from datetime import datetime

# File paths
STUDENTS_FILE = 'students.csv'
ATTENDANCE_FILE = 'attendance.csv'

# Ensure the CSV files exist
if not os.path.exists(STUDENTS_FILE):
    with open(STUDENTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name'])  # Header

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Student ID', 'Status'])  # Header

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Tracker")
        self.create_widgets()

    def create_widgets(self):
        # Create Tabs
        tab_control = ttk.Notebook(self.root)

        self.tab_manage = ttk.Frame(tab_control)
        self.tab_mark = ttk.Frame(tab_control)
        self.tab_view = ttk.Frame(tab_control)

        tab_control.add(self.tab_manage, text='Manage Students')
        tab_control.add(self.tab_mark, text='Mark Attendance')
        tab_control.add(self.tab_view, text='View Attendance')

        tab_control.pack(expand=1, fill='both')

        self.create_manage_tab()
        self.create_mark_tab()
        self.create_view_tab()

    # ---------------- Manage Students Tab ----------------
    def create_manage_tab(self):
        frame = self.tab_manage

        # Entry for Student ID
        tk.Label(frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(frame)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)

        # Entry for Student Name
        tk.Label(frame, text="Student Name:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        # Add Student Button
        btn_add = tk.Button(frame, text="Add Student", command=self.add_student)
        btn_add.grid(row=2, column=0, columnspan=2, pady=10)

        # List of Students
        self.tree_students = ttk.Treeview(frame, columns=('ID', 'Name'), show='headings')
        self.tree_students.heading('ID', text='ID')
        self.tree_students.heading('Name', text='Name')
        self.tree_students.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.load_students()

    def add_student(self):
        student_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()

        if not student_id or not name:
            messagebox.showwarning("Input Error", "Please enter both ID and Name.")
            return

        # Check for duplicate ID
        with open(STUDENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID'] == student_id:
                    messagebox.showerror("Duplicate ID", "A student with this ID already exists.")
                    return

        # Add to CSV
        with open(STUDENTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name])

        # Update Treeview
        self.tree_students.insert('', 'end', values=(student_id, name))
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        messagebox.showinfo("Success", "Student added successfully.")

    def load_students(self):
        for row in self.tree_students.get_children():
            self.tree_students.delete(row)
        with open(STUDENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tree_students.insert('', 'end', values=(row['ID'], row['Name']))

    # ---------------- Mark Attendance Tab ----------------
    def create_mark_tab(self):
        frame = self.tab_mark

        # Date selection (default to today)
        tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_date = tk.Entry(frame)
        self.entry_date.grid(row=0, column=1, padx=10, pady=10)
        self.entry_date.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Button to load students
        btn_load = tk.Button(frame, text="Load Students", command=self.load_attendance)
        btn_load.grid(row=0, column=2, padx=10, pady=10)

        # Treeview for attendance
        self.tree_attendance = ttk.Treeview(frame, columns=('ID', 'Name', 'Status'), show='headings')
        self.tree_attendance.heading('ID', text='ID')
        self.tree_attendance.heading('Name', text='Name')
        self.tree_attendance.heading('Status', text='Status')
        self.tree_attendance.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_attendance.yview)
        self.tree_attendance.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky='ns')

        # Mark Present and Absent Buttons
        btn_present = tk.Button(frame, text="Mark Present", command=lambda: self.mark_status("Present"))
        btn_present.grid(row=2, column=0, padx=10, pady=10)

        btn_absent = tk.Button(frame, text="Mark Absent", command=lambda: self.mark_status("Absent"))
        btn_absent.grid(row=2, column=1, padx=10, pady=10)

        btn_save = tk.Button(frame, text="Save Attendance", command=self.save_attendance)
        btn_save.grid(row=2, column=2, padx=10, pady=10)

    def load_attendance(self):
        date_str = self.entry_date.get().strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        # Load students
        self.attendance_data = {}
        with open(STUDENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.attendance_data[row['ID']] = {'Name': row['Name'], 'Status': 'Absent'}

        # Load existing attendance for the date
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Date'] == date_str:
                        if row['Student ID'] in self.attendance_data:
                            self.attendance_data[row['Student ID']]['Status'] = row['Status']

        # Populate Treeview
        for item in self.tree_attendance.get_children():
            self.tree_attendance.delete(item)
        for sid, info in self.attendance_data.items():
            self.tree_attendance.insert('', 'end', values=(sid, info['Name'], info['Status']))

    def mark_status(self, status):
        selected = self.tree_attendance.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a student to mark.")
            return
        for item in selected:
            self.tree_attendance.set(item, 'Status', status)

    def save_attendance(self):
        date_str = self.entry_date.get().strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        # Collect attendance data
        attendance_list = []
        for item in self.tree_attendance.get_children():
            sid, name, status = self.tree_attendance.item(item, 'values')
            attendance_list.append([date_str, sid, status])

        # Remove existing entries for the date to prevent duplicates
        temp_file = 'temp_attendance.csv'
        with open(ATTENDANCE_FILE, 'r', newline='') as f, open(temp_file, 'w', newline='') as temp_f:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(temp_f, fieldnames=['Date', 'Student ID', 'Status'])
            writer.writeheader()
            for row in reader:
                if row['Date'] != date_str:
                    writer.writerow(row)
        
        # Write back with updated attendance
        with open(temp_file, 'a', newline='') as temp_f:
            writer = csv.writer(temp_f)
            writer.writerows(attendance_list)
        
        os.replace(temp_file, ATTENDANCE_FILE)
        messagebox.showinfo("Success", "Attendance saved successfully.")

    # ---------------- View Attendance Tab ----------------
    def create_view_tab(self):
        frame = self.tab_view

        # Option to view by Date or by Student
        self.view_option = tk.StringVar(value="Date")
        tk.Radiobutton(frame, text="View by Date", variable=self.view_option, value="Date", command=self.update_view_options).grid(row=0, column=0, padx=10, pady=10)
        tk.Radiobutton(frame, text="View by Student", variable=self.view_option, value="Student", command=self.update_view_options).grid(row=0, column=1, padx=10, pady=10)

        # Frame for dynamic options
        self.view_frame = tk.Frame(frame)
        self.view_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.update_view_options()

        # Treeview for displaying attendance
        self.tree_view = ttk.Treeview(frame, show='headings')
        self.tree_view.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_view.yview)
        self.tree_view.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=3, sticky='ns')

    def update_view_options(self):
        # Clear the previous widgets in view_frame
        for widget in self.view_frame.winfo_children():
            widget.destroy()

        option = self.view_option.get()
        if option == "Date":
            tk.Label(self.view_frame, text="Select Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
            self.view_date_entry = tk.Entry(self.view_frame)
            self.view_date_entry.grid(row=0, column=1, padx=10, pady=10)
            btn_load = tk.Button(self.view_frame, text="Load", command=self.view_by_date)
            btn_load.grid(row=0, column=2, padx=10, pady=10)
        else:
            tk.Label(self.view_frame, text="Select Student ID:").grid(row=0, column=0, padx=10, pady=10)
            self.view_student_id = tk.StringVar()
            self.combo_students = ttk.Combobox(self.view_frame, textvariable=self.view_student_id)
            self.combo_students.grid(row=0, column=1, padx=10, pady=10)
            self.load_student_ids()
            btn_load = tk.Button(self.view_frame, text="Load", command=self.view_by_student)
            btn_load.grid(row=0, column=2, padx=10, pady=10)

    def load_student_ids(self):
        with open(STUDENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            student_ids = [row['ID'] for row in reader]
        self.combo_students['values'] = student_ids

    def view_by_date(self):
        date_str = self.view_date_entry.get().strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        # Set up Treeview columns
        self.tree_view['columns'] = ('ID', 'Name', 'Status')
        for col in self.tree_view['columns']:
            self.tree_view.heading(col, text=col)
            self.tree_view.column(col, width=100)

        # Clear existing data
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # Load attendance for the date
        attendance_records = {}
        with open(ATTENDANCE_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Date'] == date_str:
                    attendance_records[row['Student ID']] = row['Status']

        # Load student names
        students = {}
        with open(STUDENTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students[row['ID']] = row['Name']

        # Populate Treeview
        for sid, status in attendance_records.items():
            name = students.get(sid, "Unknown")
            self.tree_view.insert('', 'end', values=(sid, name, status))

    def view_by_student(self):
        student_id = self.view_student_id.get().strip()
        if not student_id:
            messagebox.showerror("Input Error", "Please select a student ID.")
            return

        # Set up Treeview columns
        self.tree_view['columns'] = ('Date', 'Status')
        for col in self.tree_view['columns']:
            self.tree_view.heading(col, text=col)
            self.tree_view.column(col, width=150)

        # Clear existing data
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        # Load attendance for the student
        attendance_records = []
        with open(ATTENDANCE_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Student ID'] == student_id:
                    attendance_records.append((row['Date'], row['Status']))

        # Populate Treeview
        for date, status in attendance_records:
            self.tree_view.insert('', 'end', values=(date, status))

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
