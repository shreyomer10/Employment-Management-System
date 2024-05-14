import tkinter as tk
from tkinter import messagebox

# Import your module classes
from gui_dept import DepartmentGUI
from job_GUI import job
from employee_GUI import employee
from r import reports
class MainMenu:
    def __init__(self, master):
        self.master = master
        master.title("Main Menu")

        # Configure window size and position
        master.geometry("300x250+500+200")

        # Add a welcome label
        self.welcome_label = tk.Label(master, text="Welcome to the Main Menu", font=("Helvetica", 14))
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Department Module
        self.department_button = tk.Button(master, text="Department Module", command=self.open_department, bg="lightblue")
        self.department_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Job Module
        self.job_button = tk.Button(master, text="Job Module", command=self.open_job, bg="lightgreen")
        self.job_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Employee Module
        self.employee_button = tk.Button(master, text="Employee Module", command=self.open_employee, bg="lightcoral")
        self.employee_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Reports Module
        self.reports_button = tk.Button(master, text="Reports Module", command=self.open_reports, bg="lightyellow")
        self.reports_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Exit Button
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_program, bg="salmon")
        self.exit_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Center all widgets vertically
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)

        # Center all widgets horizontally
        master.grid_columnconfigure(0, weight=1)

        # Add padding to all widgets
        for child in master.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def open_department(self):
        department_window = tk.Toplevel(self.master)
        department_gui = DepartmentGUI(department_window)

    def open_job(self):
        job_window = tk.Toplevel(self.master)
        job_gui = job(job_window)

    def open_employee(self):
        employee_window = tk.Toplevel(self.master)
        employee_gui = employee(employee_window)

    def open_reports(self):
        reports_window = tk.Toplevel(self.master)
        reports_gui = reports(reports_window)

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    root.resizable(False, False)  # Disable resizing
    menu = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()




