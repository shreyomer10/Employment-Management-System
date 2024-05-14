
import pymysql as pm
import tkinter as tk
from prettytable import PrettyTable
from tkinter import messagebox
class DepartmentGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("Department Module")

        # Entry widgets for department details
        self.dname_entry = tk.Entry(master)
        self.man_entry = tk.Entry(master)
        self.dno_entry = tk.Entry(master)

        # Buttons for Department Functions
        self.view_button = tk.Button(master, text="View All Departments", command=self.view_all_dept)
        self.view_button.grid(row=0, column=0, columnspan=2)

        self.insert_button = tk.Button(master, text="Insert Department", command=self.insert_dept)
        self.insert_button.grid(row=1, column=0, columnspan=2)

        self.update_button = tk.Button(master, text="Update Department", command=self.update_dept)
        self.update_button.grid(row=2, column=0, columnspan=2)

        self.delete_button = tk.Button(master, text="Delete Department", command=self.delete_dept)
        self.delete_button.grid(row=3, column=0, columnspan=2)

        # Output Text Area
        self.output_text = tk.Text(master, height=30, width=100)
        self.output_text.grid(row=4, column=0, columnspan=2)
        '''
    def __init__(self, master):
        self.master = master
        master.title("Department Module")
        master.configure(bg="#f0f0f0")

        # Entry widgets for department details
        self.dname_entry = tk.Entry(master, font=("Helvetica", 12))
        self.man_entry = tk.Entry(master, font=("Helvetica", 12))
        self.dno_entry = tk.Entry(master, font=("Helvetica", 12))

        # Buttons for Department Functions
        self.view_button = tk.Button(master, text="View All Departments", command=self.view_all_dept, bg="#87ceeb", fg="white", font=("Helvetica", 12))
        self.view_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.insert_button = tk.Button(master, text="Insert Department", command=self.insert_dept, bg="#90ee90", fg="white", font=("Helvetica", 12))
        self.insert_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_button = tk.Button(master, text="Update Department", command=self.update_dept, bg="#ffa500", fg="white", font=("Helvetica", 12))
        self.update_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.delete_button = tk.Button(master, text="Delete Department", command=self.delete_dept, bg="#ff6347", fg="white", font=("Helvetica", 12))
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output Text Area
        self.output_text = tk.Text(master, height=50, width=100, font=("Helvetica", 10), bg="#ffffff")
        self.output_text.grid(row=4, column=0, columnspan=2, pady=20)
'''
    def validate_input(self, *entries):
        for entry in entries:
            if not entry.get():
                messagebox.showerror("Input Error", "Please fill in all fields.")
                return False
        return True

    def validate_gender(self, gender):
        if gender.upper() not in ['M', 'F']:
            messagebox.showerror("Input Error", "Gender must be 'M' or 'F'.")
            return False
        return True

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            messagebox.showerror("Input Error", "Date format should be dd/mm/yyyy.")
            return False

    def check_exists_in_db(self, table, column, value):
        try:
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {table} WHERE {column}=%s", (value,))
            if cur.rowcount == 0:
                messagebox.showerror("Error", f"{column} '{value}' does not exist in the database.")
                return False
            return True
        except pm.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return False
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def getmaxdno(self):
        maxdno = ''
        try:
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute("SELECT max(dno) FROM dept")
            row = cur.fetchone()
            maxdno = row[0] + 1 if row[0] is not None else 1  # Set default value to 1 if no records found
        except pm.DatabaseError as e:
            print('Database Error:', e)
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
        return maxdno

    def view_all_dept(self):
        try:
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute("SELECT * FROM dept")
            data = cur.fetchall()
            table = PrettyTable(["Department No", "Department", "Manager"])
            for row in data:
                table.add_row(row)
            self.output_text.insert(tk.END, f"{table}\n")
        except pm.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def insert_dept(self):
        # Clear the output text area
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.dno_entry.grid_forget()
        self.dname_entry.grid_forget()
        self.man_entry.grid_forget()

        # Create entry widgets for department name and manager
          # Function to insert department
        tk.Label(self.master, text="Department Name:").grid(row=5, column=0)
        self.dname_entry.grid(row=5, column=1)

        tk.Label(self.master, text="Manager:").grid(row=6, column=0)
        self.man_entry.grid(row=6, column=1)
        def insert_department():
            


            dname = self.dname_entry.get()
            man = self.man_entry.get()

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                dno = self.getmaxdno()
                response = messagebox.askyesno("Confirm Insert ", f"Do you Insert department  with department Number {dno}?")
                if response == tk.YES:
                    
                    cur.execute("INSERT INTO dept (dno, dname, man) VALUES (%s, %s, %s)", (dno, dname, man))
                    con.commit()
                    self.output_text.insert(tk.END, "Department inserted successfully!\n")
                else:
                    self.output_text.insert(tk.END, "Abborted\n")
                
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Insert button for department
        insert_button = tk.Button(self.master, text="Insert", command=insert_department)
        insert_button.grid(row=7, column=0, columnspan=2)

    def update_dept(self):
        # Clear the output text area
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and delete
        self.dname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.man_entry.grid_forget()

        # Create entry widget for department number
        tk.Label(self.master, text="Department No:").grid(row=5, column=0)
        self.dno_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Manager:").grid(row=6, column=0)
        self.man_entry.grid(row=6, column=1)

        # Create entry widgets for department name and manager
               # Function to update department
        def update_department():
            


            dno = self.dno_entry.get()
            dname = self.dname_entry.get()
            man = self.man_entry.get()
            if not self.check_exists_in_db("dept", "dno", dno):
                return 


            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm UPDATE ", f"Do you want to update departmente with department Number {dno}?")
                if response == tk.YES:

                    cur.execute("UPDATE dept SET dname = %s, man = %s WHERE dno = %s", (dname, man, dno))
                    con.commit()
                    self.output_text.insert(tk.END, f"Department {dno} updated successfully!\n")
                else:
                    self.output_text.insert(tk.END, "Updation cancelled.\n")

            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Update button for department
        update_button = tk.Button(self.master, text="Update", command=update_department)
        update_button.grid(row=7, column=0, columnspan=2)

    def delete_dept(self):
        # Clear the output text area
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and update
        self.dname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.man_entry.grid_forget()
        tk.Label(self.master, text="Department No:").grid(row=5, column=0)
        self.dno_entry.grid(row=5, column=1)

        # Create entry widget for department number
              # Function to delete department
        def delete_department():
            
            dno = self.dno_entry.get()
            if not self.check_exists_in_db("emp", "dno", dno):
                return


            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm Deletion", f"Do you want to delete dEPARTMENT with dEPARTMENT Number {dno}?")
                if response == tk.YES:
                    cur.execute("DELETE FROM dept WHERE dno = %s", (dno,))
                    con.commit()
                    self.output_text.insert(tk.END, f"Department {dno} deleted successfully!\n")
                else:
                    self.output_text.insert(tk.END, "Deletion cancelled.\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Delete button for department
        delete_button = tk.Button(self.master, text="Delete", command=delete_department)
        delete_button.grid(row=7, column=0, columnspan=2)


root = tk.Tk()
gui = DepartmentGUI(root)
root.mainloop()
