
import pymysql as pm
import tkinter as tk
from tkinter import messagebox
import prettytable as pt
from datetime import datetime

class employee:
    def __init__(self, master):
        self.master = master
        master.title("Employee Module")

        # Entry widgets for employee details
        self.fname_entry = tk.Entry(master)
        self.lname_entry = tk.Entry(master)
        self.dno_entry = tk.Entry(master)
        self.gender_entry = tk.Entry(master)
        self.doj_entry = tk.Entry(master)
        self.jid_entry = tk.Entry(master)
        self.eno_entry = tk.Entry(master)

        # Buttons for employee functions
        self.view_button = tk.Button(master, text="View All Employees", command=self.showall)
        self.view_button.grid(row=0, column=0, columnspan=2)

        self.insert_button = tk.Button(master, text="Insert Employees", command=self.add)
        self.insert_button.grid(row=1, column=0, columnspan=2)

        self.update_button = tk.Button(master, text="Update Employees", command=self.update)
        self.update_button.grid(row=2, column=0, columnspan=2)

        self.delete_button = tk.Button(master, text="Delete Employees", command=self.delete)
        self.delete_button.grid(row=3, column=0, columnspan=2)

        # Output Text Area
        self.output_text = tk.Text(master, height=30, width=100)
        self.output_text.grid(row=4, column=0, columnspan=2)

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

    def getmaxeno(self):
        maxid = ''
        try:
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            qry = "select max(eno) from emp"
            cur.execute(qry)
            row = cur.fetchone()
            if row[0] is None:
                maxid = 1
            else:
                maxid = row[0] + 1
        except pm.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return maxid

    def add(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.eno_entry.grid_forget()

        # Create entry widgets for employee details
        tk.Label(self.master, text="Employee First Name:").grid(row=5, column=0)
        self.fname_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Employee Last Name:").grid(row=6, column=0)
        self.lname_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Department Number:").grid(row=7, column=0)
        self.dno_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Gender:").grid(row=8, column=0)
        self.gender_entry.grid(row=8, column=1)
        tk.Label(self.master, text="Date of Joining:").grid(row=9, column=0)
        self.doj_entry.grid(row=9, column=1)
        tk.Label(self.master, text="Job ID:").grid(row=10, column=0)
        self.jid_entry.grid(row=10, column=1)

        # Function to insert employee
        def insert_emp():
            if not self.validate_input(self.fname_entry, self.lname_entry, self.dno_entry, self.gender_entry, self.doj_entry, self.jid_entry):
                return

            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            dno = self.dno_entry.get()
            gender = self.gender_entry.get().upper()
            doj = self.doj_entry.get()
            jid = self.jid_entry.get()

            if not (self.validate_gender(gender) and self.validate_date(doj) and
                    self.check_exists_in_db("dept", "dno", dno) and
                    self.check_exists_in_db("job", "jid", jid)):
                return

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                eno = self.getmaxeno()  # Get max employee number
                qry = f"""
                INSERT INTO emp
                VALUES
                ('{eno}', '{fname}', '{lname}', '{dno}', '{gender}', '{doj}', '{jid}')
                """
                cur.execute(qry)
                con.commit()
                self.output_text.insert(tk.END, "Employee inserted successfully!\n")
            except pm.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error: {e}")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Insert button for employee
        insert_button = tk.Button(self.master, text="Insert", command=insert_emp)
        insert_button.grid(row=12, column=0, columnspan=2)

    def update(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and delete
        self.fname_entry.grid_forget()
        self.lname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.gender_entry.grid_forget()
        self.doj_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.eno_entry.grid_forget()

        # Create entry widget for employee number
        tk.Label(self.master, text="Employee No:").grid(row=5, column=0)
        self.eno_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Employee First Name:").grid(row=6, column=0)
        self.fname_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Employee Last Name:").grid(row=7, column=0)
        self.lname_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Department Number:").grid(row=8, column=0)
        self.dno_entry.grid(row=8, column=1)
        tk.Label(self.master, text="Gender:").grid(row=9, column=0)
        self.gender_entry.grid(row=9, column=1)
        tk.Label(self.master, text="Date of Joining:").grid(row=10, column=0)
        self.doj_entry.grid(row=10, column=1)
        tk.Label(self.master, text="Job ID:").grid(row=11, column=0)
        self.jid_entry.grid(row=11, column=1)

        # Function to update employee
        def update_emp():
            if not self.validate_input(self.eno_entry, self.fname_entry, self.lname_entry, self.dno_entry, self.gender_entry, self.doj_entry, self.jid_entry):
                return

            eno = self.eno_entry.get()
            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            dno = self.dno_entry.get()
            gender = self.gender_entry.get().upper()
            doj = self.doj_entry.get()
            jid = self.jid_entry.get()

            if not (self.validate_gender(gender) and self.validate_date(doj) and
                    self.check_exists_in_db("emp", "eno", eno) and
                    self.check_exists_in_db("dept", "dno", dno) and
                    self.check_exists_in_db("job", "jid", jid)):
                return

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm UPDATE ", f"Do you want to update employee with Employee Number {eno}?")
                if response == tk.YES:

                    cur.execute("UPDATE emp SET fname = %s, lname = %s, dno = %s, gender = %s, doj = %s, jid = %s WHERE eno = %s", (fname, lname, dno, gender, doj, jid, eno))
                    con.commit()
                    self.output_text.insert(tk.END, f"Employee {eno} updated successfully!\n")
                else:
                    self.output_text.insert(tk.END, "Updation cancelled.\n")
                    
            except pm.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error: {e}")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Update button for employee
        update_button = tk.Button(self.master, text="Update", command=update_emp)
        update_button.grid(row=12, column=0, columnspan=2)

    def showall(self):
        try:
            qry = """
                SELECT * FROM emp
            """
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute(qry)
            data = cur.fetchall()
            t = pt.PrettyTable(["Employee No", "First Name", "Last Name", "Department Number", "Gender", "Date of Joining", "Job ID"])
            for row in data:
                t.add_row(row)
            self.output_text.insert(tk.END, f"{t}\n")
        except pm.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def delete(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and update
        self.fname_entry.grid_forget()
        self.lname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.gender_entry.grid_forget()
        self.doj_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.eno_entry.grid_forget()

        # Create entry widget for employee number
        tk.Label(self.master, text="Employee No:").grid(row=5, column=0)
        self.eno_entry.grid(row=5, column=1)

        # Function to delete employee
        def delete_emp():
            if not self.validate_input(self.eno_entry):
                return

            eno = self.eno_entry.get()

            if not self.check_exists_in_db("emp", "eno", eno):
                return

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm Deletion", f"Do you want to delete employee with Employee Number {eno}?")
                if response == tk.YES:
                    qrydel = f"DELETE FROM emp WHERE eno = {eno}"
                    cur.execute(qrydel)
                    con.commit()
                    self.output_text.insert(tk.END, f"Employee {eno} deleted successfully!\n")
                else:
                    self.output_text.insert(tk.END, "Deletion cancelled.\n")
            except pm.DatabaseError as e:
                messagebox.showerror("Database Error", f"Error: {e}")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Delete button for employee
        delete_button = tk.Button(self.master, text="Delete", command=delete_emp)
        delete_button.grid(row=12, column=0, columnspan=2)


root = tk.Tk()
app = employee(root)
root.mainloop()


'''
import pymysql as pm
import tkinter as tk
import prettytable as pt

class employee:
    def __init__(self, master):
        self.master = master
        master.title("Employee Module")

        # Entry widgets for emp details
        self.fname_entry = tk.Entry(master)
        self.lname_entry = tk.Entry(master)
        self.dno_entry = tk.Entry(master)
        self.gender_entry = tk.Entry(master)
        self.doj_entry = tk.Entry(master)
        self.jid_entry = tk.Entry(master)
        self.eno_entry = tk.Entry(master)

        # Buttons for emp Functions
        self.view_button = tk.Button(master, text="View All Employees", command=self.showall)
        self.view_button.grid(row=0, column=0, columnspan=2)

        self.insert_button = tk.Button(master, text="Insert Employees", command=self.add)
        self.insert_button.grid(row=1, column=0, columnspan=2)

        self.update_button = tk.Button(master, text="Update Employees", command=self.update)
        self.update_button.grid(row=2, column=0, columnspan=2)

        self.delete_button = tk.Button(master, text="Delete Employees", command=self.delete)
        self.delete_button.grid(row=3, column=0, columnspan=2)

        # Output Text Area
        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.grid(row=4, column=0, columnspan=2)

    def getmaxeno(self):
        maxid = ''
        try:
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            qry = "select max(eno) from emp"
            cur.execute(qry)
            row = cur.fetchone()
            if row[0] is None:
                maxid = 1
            else:
                maxid = row[0] + 1
        except pm.DatabaseError as e:
            print('Database Error:', e)
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return maxid

    def add(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.eno_entry.grid_forget()

        # Create entry widgets for employee details
        tk.Label(self.master, text="Employee First Name:").grid(row=5, column=0)
        self.fname_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Employee Last Name:").grid(row=6, column=0)
        self.lname_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Department Number:").grid(row=7, column=0)
        self.dno_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Gender:").grid(row=8, column=0)
        self.gender_entry.grid(row=8, column=1)
        tk.Label(self.master, text="Date of Joining:").grid(row=9, column=0)
        self.doj_entry.grid(row=9, column=1)
        tk.Label(self.master, text="Job ID:").grid(row=10, column=0)
        self.jid_entry.grid(row=10, column=1)

        # Function to insert employee
        def insert_emp():
            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            dno = self.dno_entry.get()
            gender = self.gender_entry.get()
            doj = self.doj_entry.get()
            jid = self.jid_entry.get()

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                eno = self.getmaxeno()  # Get max employee number
                qry = f"""
                INSERT INTO emp
                VALUES
                ('{eno}', '{fname}', '{lname}', '{dno}', '{gender}', '{doj}', '{jid}')
                """
                cur.execute(qry)
                con.commit()
                self.output_text.insert(tk.END, "Employee inserted successfully!\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Insert button for employee
        insert_button = tk.Button(self.master, text="Insert", command=insert_emp)
        insert_button.grid(row=12, column=0, columnspan=2)

    def update(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and delete
       # self.insert_button.grid_forget()
        self.fname_entry.grid_forget()
        self.lname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.gender_entry.grid_forget()
        self.doj_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.eno_entry.grid_forget()

        # Create entry widget for employee number
        tk.Label(self.master, text="Employee No:").grid(row=5, column=0)
        self.eno_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Employee First Name:").grid(row=6, column=0)
        self.fname_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Employee Last Name:").grid(row=7, column=0)
        self.lname_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Department Number:").grid(row=8, column=0)
        self.dno_entry.grid(row=8,column=1)
        tk.Label(self.master, text="Gender:").grid(row=9, column=0)
        self.gender_entry.grid(row=9, column=1)
        tk.Label(self.master, text="Date of Joining:").grid(row=10, column=0)
        self.doj_entry.grid(row=10, column=1)
        tk.Label(self.master, text="Job ID:").grid(row=11, column=0)
        self.jid_entry.grid(row=11, column=1)


        # Function to update employee
        def update_emp():
            eno = self.eno_entry.get()
            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            dno = self.dno_entry.get()
            gender = self.gender_entry.get()
            doj = self.doj_entry.get()
            jid = self.jid_entry.get()

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                cur.execute("UPDATE emp SET fname = %s, lname = %s, dno = %s, gender = %s, doj = %s, jid = %s WHERE eno = %s", (fname, lname, dno, gender, doj, jid, eno))
                con.commit()
                self.output_text.insert(tk.END, f"Employee {eno} updated successfully!\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Update button for employee
        update_button = tk.Button(self.master, text="Update", command=update_emp)
        update_button.grid(row=12, column=0, columnspan=2)

    def showall(self):
        try:
            qry = """
                SELECT * FROM emp
            """
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute(qry)
            data = cur.fetchall()
            t = pt.PrettyTable(["Employee No", "First Name", "Last Name", "Department Number", "Gender", "Date of Joining", "Job ID"])
            for row in data:
                t.add_row(row)
            self.output_text.insert(tk.END, f"{t}\n")
        except pm.DatabaseError as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def delete(self):
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and update
        self.fname_entry.grid_forget()
        self.lname_entry.grid_forget()
        self.dno_entry.grid_forget()
        self.gender_entry.grid_forget()
        self.doj_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.eno_entry.grid_forget()

        # Create entry widget for employee number
        tk.Label(self.master, text="Employee No:").grid(row=5, column=0)
        self.eno_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Employee First Name:").grid(row=6, column=0)
        self.fname_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Employee Last Name:").grid(row=7, column=0)
        self.lname_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Department Number:").grid(row=8, column=0)
        self.dno_entry.grid(row=8, column=1)
        tk.Label(self.master, text="Gender:").grid(row=9, column=0)
        self.gender_entry.grid(row=9, column=1)
        tk.Label(self.master, text="Date of Joining:").grid(row=10, column=0)
        self.doj_entry.grid(row=10, column=1)
        tk.Label(self.master, text="Job ID:").grid(row=11, column=0)
        self.jid_entry.grid(row=11, column=1)




        # Function to delete employee
        def delete_emp():
            eno = self.eno_entry.get()

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                qrydel = f"""
                    DELETE FROM emp
                    WHERE eno = {eno}
                """
                cur.execute(qrydel)
                con.commit()
                self.output_text.insert(tk.END, f"Employee {eno} deleted successfully!\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Delete button for employee
        delete_button = tk.Button(self.master, text="Delete", command=delete_emp)
        delete_button.grid(row=12, column=0, columnspan=2)


root = tk.Tk()
gui = employee(root)
root.mainloop()
'''
