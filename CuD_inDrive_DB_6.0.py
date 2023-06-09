from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pymysql
from io import BytesIO
from PIL import Image
from datetime import datetime
from tkinter import ttk
import tkinter as tk

user=input('Enter ID:')
user=user.lower().strip()
pw=input('Enter Password:')
pw=pw.lower().strip()

win = Tk()
win.geometry('1920x1080')
win.configure(bg='#7e499d')
win.title('CuD inDrive_DB')

columns = ('reg_no','date','phase','payment_by','sl_no')

tree = ttk.Treeview(win,columns=columns, show='headings',height=25)
tree.place(x=700,y=50)

tree.column("reg_no",anchor='s', stretch='NO', width=100)
tree.column("date",anchor='s', stretch='NO', width=100)
tree.column("phase",anchor='s', stretch='NO', width=120)
tree.column("payment_by",anchor='s', stretch='NO', width=100)
tree.column("sl_no",anchor='s', stretch='NO', width=100)

tree.heading('reg_no', text='Reg no')
tree.heading('date', text='Date')
tree.heading('phase', text='Phase')
tree.heading('payment_by', text='Payment by')
tree.heading('sl_no', text='Sl no')

style = ttk.Style(win) 
style.theme_use("clam") # set theam to clam
style.configure("Treeview", background="black", 
                fieldbackground="black", foreground="white")
style.configure('Treeview.Heading', background="PowderBlue")

def browse_path():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    e3.delete(0, END)
    e3.insert(0, path)

def submit():
    try:
        reg = e1.get()
        reg=reg.strip()
        date = e2.get()
        date=date.strip()
        img1 = e3.get()
        img1 = img1.strip('""')
        phase= combo.get()
        phase= phase.strip()

        date_obj = datetime.strptime(date, "%d-%m-%Y")
        date = date_obj.strftime("%Y%m%d")
        date=int(date)

        with open(img1,'rb') as image:
            img=image.read()

        conobj = pymysql.connect(host='192.168.1.13', port=3306, user=user, password=pw, database='indrive')
        curobj = conobj.cursor()

        curobj.execute('INSERT INTO indrive(reg_no,date,img,phase,payment_by) VALUES(%s, %s, %s,%s,%s)', (reg, date, img,phase,user))
        messagebox.showinfo('Register', 'Success!')
        conobj.commit()
        conobj.close()

        e1.delete(0,'end')
        e3.delete(0,'end')
        e1.focus()

        conobj = pymysql.connect(host='192.168.1.13', port=3306, user=user, password=pw, database='indrive')
        for item in tree.get_children():
            tree.delete(item)
        
        with conobj.cursor() as cursor:
            cursor.execute('SELECT reg_no,date,phase,payment_by,sl_no FROM indrive order by sl_no desc')
            rows = cursor.fetchall()

        info=[]    
        for row in rows:
            info.append(row)

        for i in info:
            tree.insert('', tk.END, values=i)

        conobj.close()
    except Exception as e:
        messagebox.showinfo('Register', 'Something went wrong: ' + str(e))

def search():
    try:
        reg1 = e4.get()
        reg1=reg1.strip()
        date1 = e5.get()
        date1=date1.strip()

        date_obj = datetime.strptime(date1, "%d-%m-%Y")
        date1 = date_obj.strftime("%Y%m%d")
        date1=int(date1)

        conobj = pymysql.connect(host='192.168.1.13', port=3306, user=user, password=pw, database='indrive')
        curobj = conobj.cursor()

        curobj.execute("SELECT img FROM indrive where reg_no=%s and date=%s",(reg1,date1))
        result = curobj.fetchone()
        blob_data = result[0]

        conobj.commit()
        conobj.close()

        image_stream = BytesIO(blob_data)
        image = Image.open(image_stream)
        image.show()

        e4.delete(0,'end')
        e5.delete(0,'end')
        e4.focus()
    except Exception as e:
        messagebox.showinfo('Search', 'Something went wrong: ' + str(e))

def display_table():
    try:
        conobj = pymysql.connect(host='192.168.1.13', port=3306, user=user, password=pw, database='indrive')
        for item in tree.get_children():
            tree.delete(item)
        
        with conobj.cursor() as cursor:
            cursor.execute('SELECT reg_no,date,phase,payment_by,sl_no FROM indrive order by sl_no desc')
            rows = cursor.fetchall()

        info=[]    
        for row in rows:
            info.append(row)

        for i in info:
            tree.insert('', tk.END, values=i)

        conobj.close()
 
    except Exception as e:
        messagebox.showinfo('Register', 'Something went wrong: ' + str(e))

l2 = Label(win, text='Date', font=('', 15), bg='#7e499d')
l2.place(x=70, y=100)

e2 = Entry(win, font=('', 15))
e2.place(x=250, y=100)
        
l1 = Label(win, text='Registration No.', font=('', 15), bg='#7e499d')
l1.place(x=70, y=150)

e1 = Entry(win, font=('', 15))
e1.place(x=250, y=150)

l3 = Label(win, text='Selected Path:', font=('', 15), bg='#7e499d')
l3.place(x=70, y=200)

e3 = Entry(win, font=('', 15))
e3.place(x=250, y=200)

browse_button = Button(win, text="Browse", font=('', 10), command=browse_path)
browse_button.place(x=500, y=200)

submit_button = Button(win, text="Submit", font=('', 12), command=submit)
submit_button.place(x=250, y=250)

l4 = Label(win, text='Registration No.', font=('', 15), bg='#7e499d')
l4.place(x=70, y=400)

e4 = Entry(win, font=('', 15))
e4.place(x=250, y=400)

l5 = Label(win, text='Date', font=('', 15), bg='#7e499d')
l5.place(x=70, y=450)

e5 = Entry(win, font=('', 15))
e5.place(x=250, y=450)

submit_button = Button(win, text="Search", font=('', 12),command=search)
submit_button.place(x=250, y=500)

l6 = Label(win, text='Phase', font=('', 15), bg='#7e499d')
l6.place(x=70, y=50)

combo = ttk.Combobox(win, font=('', 14))
combo['values'] = ('inDrive Gurgaon', 'Delhi NCR Phase 2', 'Delhi NCR Phase 3', 'Delhi NCR Phase 4',
                   'Delhi NCR Phase 5','LUDHIANA PHASE 1','LUDHIANA PHASE 2','LUDHIANA PHASE 3',
                   'Lucknow Phase 1','Lucknow Phase 2','Lucknow Phase 3','Bhopal Phase 1',
                   'B Ops. Delhi CB','B Ops. Noida CB','B Ops. Gurgaon CB','B Ops. Lucknow CB','B Ops. Chennai CB','Challan')
combo.set('Select an option')
combo.place(x=250, y=50)

treeScroll = ttk.Scrollbar(win)
treeScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeScroll.set)
treeScroll.pack(side= 'right', fill= 'both')
tree.place(x=700,y=50)
        
fetch_button = tk.Button(win, text='Fetch Table',font=('', 11), command=display_table)
fetch_button.place(x=700,y=600)

win.mainloop()
