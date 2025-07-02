from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox
from tkinter import filedialog

import ttkthemes.themed_tk
from PIL import Image, ImageTk
import pymysql
import pandas
import mysql.connector


#functionality part

def iexit():
    result=messagebox.askyesno("Confirmation", "Do you want to Exit ?")
    if result:
        root.destroy()
    else:
        pass
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','D.O.B'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data Saved Succesfully!')

def update_student():
    def update_data():
        query=r"UPDATE STUDENT SET name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s WHERE id=%s"
        mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),idEntry.get()))
        con.commit()
        messagebox.showinfo('Sucess',f'Id {idEntry.get()} has been modified successfully')
        update_window.destroy()
        show_student()


    update_window=Toplevel()
    update_window.title("Update Student Details")
    update_window.resizable(False,False)
    update_window.grab_set()

    idLabel=Label(update_window,text="ID",font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(update_window,font=('times new roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,padx=15,pady=10)

    nameLabel = Label(update_window, text="Name", font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15,sticky=W)
    nameEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    nameEntry.grid(row=1, column=1, padx=15, pady=10)

    phoneLabel = Label(update_window, text="Phone", font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15,sticky=W)
    phoneEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    phoneEntry.grid(row=2, column=1, padx=15, pady=10)

    emailLabel = Label(update_window, text="Email", font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15,sticky=W)
    emailEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    emailEntry.grid(row=3, column=1, padx=15, pady=10)

    addressLabel = Label(update_window, text="Address", font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15,sticky=W)
    addressEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    addressEntry.grid(row=4, column=1, padx=15, pady=10)

    genderLabel = Label(update_window, text="Gender", font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15,sticky=W)
    genderEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    genderEntry.grid(row=5, column=1, padx=15, pady=10)

    dobLabel = Label(update_window, text="D.O.B", font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15,sticky=W)
    dobEntry = Entry(update_window, font=('times new roman', 15, 'bold') ,width=24)
    dobEntry.grid(row=6, column=1, padx=15, pady=10)

    update_studentButton=ttk.Button(update_window, text="UPDATE STUDENT DETAILS", command=update_data)
    update_studentButton.grid(row=7, columnspan=2, padx=15, pady=10)

    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    listdata=content['values']
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0,listdata[1])
    phoneEntry.insert(0,listdata[2])
    emailEntry.insert(0,listdata[3])
    addressEntry.insert(0,listdata[4])
    genderEntry.insert(0,listdata[5])
    dobEntry.insert(0,listdata[6])






def show_student():
    query = r"SELECT * FROM STUDENT "
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert("", END, values=data)


def delete_student():
    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query=r"DELETE FROM STUDENT WHERE Id=%s"
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo("Deleted",f'Data of Id {content_id} is deleted successfully')
    query=r"SELECT * FROM STUDENT "
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert("",END,values=data)


def search_student():
    def search_data():
        query=r"SELECT * FROM student WHERE id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s"
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
        studentTable.delete(*studentTable.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('',END,values=data)

    search_window = Toplevel()
    search_window.title("Search Student")
    search_window.resizable(False, False)
    search_window.grab_set()
    idLabel = Label(search_window, text="ID", font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, padx=15, pady=10)

    nameLabel = Label(search_window, text="Name", font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, padx=15, pady=10)

    phoneLabel = Label(search_window, text="Phone", font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, padx=15, pady=10)

    emailLabel = Label(search_window, text="Email", font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, padx=15, pady=10)

    addressLabel = Label(search_window, text="Address", font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, padx=15, pady=10)

    genderLabel = Label(search_window, text="Gender", font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, padx=15, pady=10)

    dobLabel = Label(search_window, text="D.O.B", font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, padx=15, pady=10)

    add_studentButton = ttk.Button(search_window, text="SEARCH STUDENT", command=search_data)
    add_studentButton.grid(row=7, columnspan=2, padx=15, pady=10)



def add_student():
    def add_data():
        if(idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='' ):
            messagebox.showerror("Error","All fields are required!",parent=add_window)

        else:
            currentdate = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            try:
                query = r"INSERT INTO STUDENT(id, name, mobile, email, address, gender, dob) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(query,
                                 (idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))

                con.commit()

                result=messagebox.askyesno('Confirmation','Data Added Successfully.Do you want to clean the form?')
                if result==True:
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    phoneEntry.delete(0,END)
                    emailEntry.delete(0,END)
                    addressEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    dobEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox.showerror("Error","Id cannot be repeated!",parent=add_window)
                return



            query=r"SELECT * FROM STUDENT"
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                data_list=list(data)
                studentTable.insert('',END,values=data_list)




    add_window=Toplevel()
    add_window.title("Add Student")
    add_window.resizable(False,False)
    add_window.grab_set()
    idLabel=Label(add_window,text="ID",font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('times new roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,padx=15,pady=10)

    nameLabel = Label(add_window, text="Name", font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15,sticky=W)
    nameEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    nameEntry.grid(row=1, column=1, padx=15, pady=10)

    phoneLabel = Label(add_window, text="Phone", font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15,sticky=W)
    phoneEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    phoneEntry.grid(row=2, column=1, padx=15, pady=10)

    emailLabel = Label(add_window, text="Email", font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15,sticky=W)
    emailEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    emailEntry.grid(row=3, column=1, padx=15, pady=10)

    addressLabel = Label(add_window, text="Address", font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15,sticky=W)
    addressEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    addressEntry.grid(row=4, column=1, padx=15, pady=10)

    genderLabel = Label(add_window, text="Gender", font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15,sticky=W)
    genderEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    genderEntry.grid(row=5, column=1, padx=15, pady=10)

    dobLabel = Label(add_window, text="D.O.B", font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15,sticky=W)
    dobEntry = Entry(add_window, font=('times new roman', 15, 'bold') ,width=24)
    dobEntry.grid(row=6, column=1, padx=15, pady=10)

    add_studentButton=ttk.Button(add_window, text="ADD STUDENT", command=add_data)
    add_studentButton.grid(row=7, columnspan=2, padx=15, pady=10)



def connect_database():
    def connect():
        global mycursor,con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passEntry.get())
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Connected to MySQL Server',parent=connectWindow)
            connectWindow.destroy()
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
        except:
              messagebox.showerror("Error", "Invalid Details",parent=connectWindow)
              return
        query = r"CREATE DATABASE IF NOT EXISTS studentmanagementsystem"
        mycursor.execute(query)
        query=r"USE studentmanagementsystem"
        mycursor.execute(query)
        query= r"CREATE TABLE IF NOT EXISTS student(id int not null primary key,name varchar(30),mobile varchar(30),email varchar(30),address varchar(100),gender varchar(30),dob varchar(20))"
        mycursor.execute(query)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.title('Database Connection')
    connectWindow.geometry('500x250+730+230')
    connectWindow.resizable(False,False)

    hostnmameLabel=Label(connectWindow, text='Host Name', font=('Helvetica', 20,'bold'))
    hostnmameLabel.grid(column=0, row=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman', 15,'bold'),bd=2)
    hostEntry.grid(column=1, row=0,padx=40,pady=20)

    usernmameLabel = Label(connectWindow, text='User Name', font=('Helvetica', 20, 'bold'))
    usernmameLabel.grid(column=0, row=1, padx=20)

    userEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    userEntry.grid(column=1, row=1, padx=40, pady=20)

    passLabel = Label(connectWindow, text='Password', font=('Helvetica', 20, 'bold'))
    passLabel.grid(column=0, row=2, padx=20)

    passEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passEntry.grid(column=1, row=2, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(columnspan=2, row=3)




count=0
text=''

def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)



#GUI part

root=ttkthemes.ThemedTk()

root.config(bg='cornflowerblue')

root.get_themes()
root.set_theme('radiance')

root.geometry('1523x800+0+0')
root.resizable(False,False)
root.title('Student Management System')


datetimeLabel=Label(root,font=('times new roman',18),bg='cornflowerblue',fg='black')
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,font=('times new roman',28),width=53,bg='cornflowerblue',fg='black')
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect Database',cursor='hand2',command=connect_database)
connectButton.place(x=1300,y=0)

leftFrame=Frame(root,bg='cornflowerblue')
leftFrame.place(x=50,y=80,width=300,height=600)

logo_Image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_Image)
logo_Label.grid(row=0,column=0,columnspan=2,padx=5,pady=15)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,cursor='hand2',state=DISABLED,command=add_student)
addstudentButton.grid(row=1,column=0,padx=5,pady=10)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,cursor='hand2',state=DISABLED,command=search_student)
searchstudentButton.grid(row=2,column=0,padx=5,pady=10)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,cursor='hand2',state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,padx=5,pady=10)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,cursor='hand2',state=DISABLED,command=update_student)
updatestudentButton.grid(row=4,column=0,padx=5,pady=10)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,cursor='hand2',state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,padx=5,pady=10)

exportstudentButton=ttk.Button(leftFrame,text='Export Data',width=25,cursor='hand2',state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,padx=5,pady=10)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,cursor='hand2',command=iexit)
exitButton.grid(row=7,column=0,padx=5,pady=10)

rightFrame=Frame(root,bg='black')
rightFrame.place(x=400,y=80,width=1100,height=600)
rightFrame.config(bg='black')

scrollbarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollbarY=Scrollbar(rightFrame,orient=VERTICAL)


studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile No.','Email','Address','Gender','D.O.B'),xscrollcommand=scrollbarX.set,yscrollcommand=scrollbarY.set)
scrollbarX.config(command=studentTable.xview)
scrollbarY.config(command=studentTable.yview)

scrollbarX.pack(side=BOTTOM,fill=X)
scrollbarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=True)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No.',text='Mobile No.')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')

studentTable.column('Id',anchor=CENTER)
studentTable.column('Name',anchor=CENTER)
studentTable.column('Mobile No.',anchor=CENTER)
studentTable.column('Email',anchor=CENTER)
studentTable.column('Address',anchor=CENTER)
studentTable.column('Gender',anchor=CENTER)
studentTable.column('D.O.B',anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=30,font=('Times New Roman',15))
style.configure('Treeview.Heading',font=('Times New Roman',15,'bold'))



studentTable.config(show='headings')


root.mainloop()

