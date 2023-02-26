import pandas
from tkinter import *
from tkinter import messagebox
import os
import random
import pyperclip
csv_file = "passwords_list.csv"


class PasswordGenerate():

    def __init__(self):
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.minsize(width=500, height=500)
        self.canvas = Canvas(width=200, height=200)
        self.img = PhotoImage(file="logo.png")
        self.host_label = Label(text="Website/Host")
        self.username_label = Label(text="Email/username")
        self.password_label = Label(text="Password")
        self.input_host = Entry(width=35)
        self.input_password = Entry(width=18)
        self.input_name = Entry(width=35)
        self.generate_button = Button(text="Generate Password", command=self.generator)
        self.add_button = Button(text="Add", width=33, command=self.save_password)
        self.s_button = Button(text="Search", width=33, command=self.search)
        self.u_button = Button(text="Update", width=33, command=self.update)
        self.password = ""
        global csv_file
        self.p_file = csv_file

    def generator(self):

        self.password = ""
        self.input_password.delete(0, END)

        letters = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ]
        numbers = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        symbols = [ '!', '#', '$', '%', '&', '(', ')', '*', '+' ]

        password_list = [ random.choice(letters) for _ in range(random.randint(8, 10)) ]
        password_list += [ random.choice(numbers) for _ in range(random.randint(2, 4)) ]
        password_list += [ random.choice(symbols) for _ in range(random.randint(2, 4)) ]

        random.shuffle(password_list)
        self.password = "".join(password_list)

        self.input_password.insert(0, string=self.password)
        pyperclip.copy(self.password)

    def save_password(self):

        if not os.path.isfile(self.p_file):
            df = pandas.DataFrame(columns=[ "Host", "Username", "Password" ])
            df.to_csv(self.p_file)

        df = pandas.read_csv(self.p_file)

        host_name = self.input_host.get()
        username = self.input_name.get()
        password = self.input_password.get()

        if len(host_name) == 0 or len(password) == 0:
            messagebox.showwarning(title="Incomplete", message="Please make sure you haven't left any fields empty")
        else:
            data = {"Host": [host_name], "Username": [username], "Password": [password]}
            is_ok = messagebox.askokcancel(title=host_name, message=f"These are the details entered: "
                                                                    f"\nUsername: {username} \nPassword:{password}")
            if is_ok:
                new_data = pandas.DataFrame(data)
                df = pandas.concat([df, new_data])
                df.to_csv(self.p_file, index=False)
                self.input_host.delete(0, END)
                self.input_name.delete(0, END)
                self.input_password.delete(0, END)
                self.input_host.focus()

    def search(self):
        if not os.path.isfile(self.p_file):
            messagebox.showwarning(title="Not Exist",message="File not found!!")
        else:
            self.input_name.delete(0,END)
            self.input_password.delete(0,END)
            s_host = self.input_host.get()
            s_data = pandas.read_csv(self.p_file)
            s_hosts = s_data.loc[s_data['Host'] == s_host]
            s_username = s_hosts['Username'].item()
            s_password = s_hosts['Password'].item()
            self.input_name.insert(0, string=s_username)
            self.input_password.insert(0, string=s_password)
            pyperclip.copy(s_password)

    def update(self):
        u_host = self.input_host.get()
        u_username = self.input_name.get()
        u_password = self.input_password.get()
        print(u_host,u_username,u_password)
        u_data = pandas.read_csv(self.p_file)
        u_data.loc[u_data['Host'] == u_host, 'Username'] = u_username
        u_data.loc[u_data['Host'] == u_host, 'Password'] = u_password
        u_data.to_csv(self.p_file, index=False)

    def add_ui(self):
        self.window.config(padx=50, pady=50)
        self.canvas.create_image(100, 100, image=self.img)
        self.canvas.grid(row=0, column=1)

        self.host_label.grid(row=1, column=0)
        self.username_label.grid(row=2, column=0)
        self.password_label.grid(row=3, column=0)
        self.input_host.focus()

        self.input_host.grid(row=1, column=1, columnspan=2)
        self.input_name.grid(row=2, column=1, columnspan=2)
        self.input_password.grid(row=3, column=1)

        self.generate_button.grid(row=3, column=2)
        self.add_button.grid(row=4, column=1, columnspan=2)
        self.s_button.grid(row=5,column=1, columnspan=2)
        self.u_button.grid(row=6,column=1, columnspan=2)

        self.window.mainloop()


if __name__ == "__main__":
    add = PasswordGenerate()
    add.add_ui()
