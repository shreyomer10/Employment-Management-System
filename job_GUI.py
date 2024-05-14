import pymysql as pm
import tkinter as tk
import prettytable as pt
from tkinter import messagebox

class job:
    def __init__(self,master):
        self.master = master
        master.title("JOB Module")

        self.jobid_entry = tk.Entry(master)
        self.jobname_entry = tk.Entry(master)
        self.basicsal_entry = tk.Entry(master)
        self.comm_entry = tk.Entry(master)

        self.view_button = tk.Button(master, text="View All jobs", command=self.viewalljob)
        self.view_button.grid(row=0, column=0, columnspan=2)

        self.insert_button = tk.Button(master, text="Insert new job", command=self.insert_new_job)
        self.insert_button.grid(row=1, column=0, columnspan=2)

        self.update_button = tk.Button(master, text="Update job", command=self.updatejobb)
        self.update_button.grid(row=2, column=0, columnspan=2)

        self.delete_button = tk.Button(master, text="Delete job ", command=self.dell)
        self.delete_button.grid(row=3, column=0, columnspan=2)
        self.output_text = tk.Text(master, height=30, width=100)
        self.output_text.grid(row=4, column=0, columnspan=2)
    def validate_input(*entries):
        for entry in entries:
            if not entry.get():
                messagebox.showerror("Input Error", "Please fill in all fields.")
                return False
        return True

    @staticmethod
    def validate_gender(gender):
        if gender.upper() not in ['M', 'F']:
            messagebox.showerror("Input Error", "Gender must be 'M' or 'F'.")
            return False
        return True

    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            messagebox.showerror("Input Error", "Date format should be dd/mm/yyyy.")
            return False

    @staticmethod
    def validate_float(value):
        try:
            float(value)
            return True
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid float value.")
            return False

    @staticmethod
    def check_exists_in_db(table, column, value):
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
    def clear_input_fields(self):
        # Clear all input fields
        self.jobname_entry.delete(0, tk.END)
        self.jobid_entry.delete(0, tk.END)
        self.basicsal_entry.delete(0, tk.END)
        self.comm_entry.delete(0, tk.END)
     

    def getmaxjid(self):
        maxid=''
        try:
            con=pm.connect(user="root",password="root",host='localhost',database="emp")
            cur=con.cursor()
            qry="select max(jid) from job"
            cur.execute(qry) 
            row=cur.fetchone() #(None,)
            if row[0]==None:
                maxid=1
            else:
                maxid=row[0]+1
        except pm.DatabaseError as e:
            con.rollback()
            print(' '*gapvalue,'Database Error : ',e)
        finally:
            if cur:
                cur.close()
            if con:
                con.close()
            return maxid

    def viewalljob(self):
        try:
            qry = """
                SELECT * FROM job
            """
            con = pm.connect(user="root", password="root", host='localhost', database="emp")
            cur = con.cursor()
            cur.execute(qry)
            data = cur.fetchall()
            t = pt.PrettyTable(["jid","jobname","salary","commision"])
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

    def insert_new_job(self):
        self.clear_input_fields()
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for update and delete
        self.jobid_entry.grid_forget()

        # Create entry widgets for employee details
        tk.Label(self.master, text="Job  Name:").grid(row=5, column=0)
        self.jobname_entry.grid(row=5, column=1)

        tk.Label(self.master, text="Salary:").grid(row=6, column=0)
        self.basicsal_entry.grid(row=6, column=1)
        tk.Label(self.master, text="Commision").grid(row=7, column=0)
        self.comm_entry.grid(row=7, column=1)

        # Function to insert employee
        def insert_job():
            jobname = self.jobname_entry.get()
            basicsal = self.basicsal_entry.get()
            comm = self.comm_entry.get()
            if not ( self.validate_float(basicsal) and self.validate_float(comm)):
                
                return

            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                
                jid = self.getmaxjid()
                # Get max employee number
                qry=f""" INSERT INTO job
                     values
                     ({jid},"{jobname}",{basicsal},{comm})
                     """
                cur.execute(qry)
                con.commit()
                self.output_text.insert(tk.END, f"joB {jid} updated successfully!\n")
            except pm.DatabaseError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()

        # Insert button for employee
        insert_button = tk.Button(self.master, text="Insert", command=insert_job)
        insert_button.grid(row=11, column=0, columnspan=2)

    def dell(self):
        self.clear_input_fields()
        self.output_text.delete('1.0', tk.END)

        # Remove entry fields for insert and update
        self.jobid_entry.grid_forget()
        self.jobname_entry.grid_forget()
        self.basicsal_entry.grid_forget()
        self.comm_entry.grid_forget()
        

        # Create entry widget for employee number
        tk.Label(self.master, text="Job No:").grid(row=5, column=0)
        self.jobid_entry.grid(row=5, column=1)
        '''
        tk.Label(self.master, text="Job  Name:").grid(row=6, column=0)
        self.jobname_entry.grid(row=6, column=1)

        tk.Label(self.master, text="Salary:").grid(row=7, column=0)
        self.basicsal_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Commision").grid(row=8, column=0)
        self.comm_entry.grid(row=8, column=1)'''

        # Function to delete employee
        def delete_job():
            
            jid = self.jobid_entry.get()
            if not (self.check_exists_in_db("job", "jid", jid)):
                return


            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm Deletion", f"Do you want to delete JOb with JOB Number {jid}?")
                if response == tk.YES:

                    qrydel = f"""
                        DELETE FROM job
                        WHERE jid = {jid}
                    """
                    cur.execute(qrydel)
                    con.commit()
                    self.output_text.insert(tk.END, f"JOb {jid} deleted successfully!\n")
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

        # Delete button for employee
        delete_button = tk.Button(self.master, text="Delete", command=delete_job)
        delete_button.grid(row=11, column=0, columnspan=2)

    def updatejobb(self):
        self.output_text.delete('1.0', tk.END)
        
        self.jobid_entry.grid_forget()
        self.jobname_entry.grid_forget()
        self.basicsal_entry.grid_forget()
        self.comm_entry.grid_forget()
        
        tk.Label(self.master, text="Job No:").grid(row=5, column=0)
        self.jobid_entry.grid(row=5, column=1)
        tk.Label(self.master, text="Job  Name:").grid(row=6, column=0)
        self.jobname_entry.grid(row=6, column=1)

        tk.Label(self.master, text="Salary:").grid(row=7, column=0)
        self.basicsal_entry.grid(row=7, column=1)
        tk.Label(self.master, text="Commision").grid(row=8, column=0)
        self.comm_entry.grid(row=8, column=1)
        def update_job():
            jid = self.jobid_entry.get()
            jobname = self.jobname_entry.get()
            basicsal = self.basicsal_entry.get()
            comm = self.comm_entry.get()

            if not (self.check_exists_in_db("job", "jid", jid) and self.validate_float(basicsal) and  self.validate_float(comm)):
                return


            try:
                con = pm.connect(user="root", password="root", host='localhost', database="emp")
                cur = con.cursor()
                response = messagebox.askyesno("Confirm Update", f"Do you want to update datails of job with job Number {jid}?")
                if response == tk.YES:
                        
                    
                    cur.execute("UPDATE job SET jobname = %s, salary = %s, commision = %s WHERE jid = %s",(jobname, basicsal, comm, jid))
                    con.commit()
                    self.output_text.insert(tk.END, f"Job {jid} updated successfully!\n")
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


        # Update button for employee
        update_button = tk.Button(self.master, text="Update", command=update_job)
        update_button.grid(row=11, column=0, columnspan=2)
    


  
root = tk.Tk()
gui = job(root)
root.mainloop()
  


       
    
    
