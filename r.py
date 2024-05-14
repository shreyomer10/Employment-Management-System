import pymysql as pm
import sys
from pygame import mixer              
import prettytable as pt
import time
import tkinter as tk
from tkinter import messagebox

class reports:
 
    def __init__(self, master):  # Corrected constructor name
        self.master = master
        master.title("REPORTS")
        self.dno_entry = tk.Entry(master)
        self.eno_entry = tk.Entry(master)
        self.jid_entry = tk.Entry(master)

        self.view_button = tk.Button(master, text="View Department vise employess", command=self.searchbydept)
        self.view_button.grid(row=0, column=0, columnspan=2)

        self.insert_button = tk.Button(master, text="View JOB vise employess", command=self.searchbyjobid)
        self.insert_button.grid(row=1, column=0, columnspan=2)

        self.update_button = tk.Button(master, text="Search Employee by Emp ID", command=self.searchbyeno)
        self.update_button.grid(row=2, column=0, columnspan=2)

        # Output Text Area
        self.output_text = tk.Text(master, height=30, width=120)
        self.output_text.grid(row=4, column=0, columnspan=2)



    
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

    def searchbyeno(self):
        
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.eno_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.dno_entry.grid_forget()
        tk.Label(self.master, text="Employee No:").grid(row=5, column=0)
        self.eno_entry.grid(row=5, column=1)
        def search_eno():
            
            eno = self.eno_entry.get()
            if not self.check_exists_in_db("emp", "eno", eno):
                return
            
            try:
                qry=f"""
                    select *
                    from emp
                    where eno={eno} 
            """
                con=pm.connect(user="root",password="root",host='localhost',database="emp")
                cur=con.cursor()
                cur.execute(qry)
                data=cur.fetchall()
                r=['eno','fname','lname','dno','gender','doj','jobid' ]
                t=pt.PrettyTable(r)
              
                for i in data:
                    
                    t.add_row(i)
                
                self.output_text.insert(tk.END, f"{t}\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()
        delete_button = tk.Button(self.master, text="SHOW", command=search_eno)
        delete_button.grid(row=7, column=0, columnspan=2)

            

    def searchbydept(self):
        
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.eno_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.dno_entry.grid_forget()
        tk.Label(self.master, text="DEPARTMENT NUMBER:").grid(row=5, column=0)
        self.dno_entry.grid(row=5, column=1)
        def search_dno():
            
            dno = self.dno_entry.get()
            if not self.check_exists_in_db("dept", "dno", dno):
                return
            try:
                
                qry = f"""
    SELECT emp.*, job.*
    FROM emp
    INNER JOIN dept ON emp.dno = dept.dno
    INNER JOIN job ON emp.jid = job.jid
    WHERE emp.dno = {dno}
"""

                con=pm.connect(user="root",password="root",host='localhost',database="emp")
                cur=con.cursor()
                cur.execute(qry)
                data=cur.fetchall()
                
                print(data)
                
                r=['eno','fname','lname','dno','gender','doj','jobid', "jobeid","jobname","salary","commision"]
                t=pt.PrettyTable(r)

                for i in data:

                    t.add_row(i)

                self.output_text.insert(tk.END, f"{t}\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        delete_button = tk.Button(self.master, text="SHOW", command=search_dno)
        delete_button.grid(row=7, column=0, columnspan=2)

    def searchbyjobid(self):
        self.eno_entry.grid_forget()
        self.jid_entry.grid_forget()
        self.dno_entry.grid_forget()
        tk.Label(self.master, text="JOB ID:").grid(row=5, column=0)
        self.jid_entry.grid(row=5, column=1)
        def search_jobid():
            
            jid = self.jid_entry.get()
            if not self.check_exists_in_db("job", "jid", jid):
                return
            try:
                qry=f""" select *
                    from emp NATURAL JOIN job
                    WHERE jid={jid}
                """
                con=pm.connect(user="root",password="root",host='localhost',database="emp")
                cur=con.cursor()
                cur.execute(qry)
                data=cur.fetchall()
                r=['Jobid','eno','fname',"lname",'dno','gender','doj' ,"jobname","salary","commision"]
                t=pt.PrettyTable(r)
                for i in data:
                    
                    t.add_row(i)
                
                self.output_text.insert(tk.END, f"{t}\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        delete_button = tk.Button(self.master, text="SHOW", command=search_jobid)
        delete_button.grid(row=7, column=0, columnspan=2)



root = tk.Tk()
gui = reports(root)
root.mainloop()
