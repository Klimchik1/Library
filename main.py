import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db, auth
import math

# From Doc - https://firebase.google.com/docs/database/admin/start?authuser=1#python
cred = credentials.Certificate("serviceAccount.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://library-school-project-8aebb-default-rtdb.firebaseio.com/'
})

API_KEY = 'AIzaSyBNAJ7og35wwPcjIsF_ZTHFKCz48m0ylUg'


def firebaseRegister(email, password, fullName):
    user = auth.create_user(
        email=email,
        password=password,
        display_name=fullName
    )
    messagebox.showinfo("Success", "User was registered!")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library Manager')
        self.geometry('900x600')
        self.resizable(True, True)

        self.buildFrames()
        self.showFrame(LoginFrame)

    def buildFrames(self):
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def showFrame(self, frameClass):
        frame = self.frames[frameClass]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def loginButtonTap(self):
        email = self.email.get().strip()
        password = self.password.get().strip()

        if len(email) > 0 and len(password) > 0:
            user = auth.get_user_by_email(email)
            print(user.uid)

    def _build(self):
        pad = 10
        frm = ttk.Frame(self)
        frm.pack(padx=pad, pady=pad)
        ttk.Label(frm, text="Email:").grid(column=0, row=0, sticky='e')
        self.email = ttk.Entry(frm, width=40)
        self.email.grid(column=1, row=0)
        ttk.Label(frm, text="Password:").grid(column=0, row=1, sticky='e')
        self.password = ttk.Entry(frm, width=40)
        self.password.grid(column=1, row=1)
        loginBtn = ttk.Button(frm, text="Login", command=self.loginButtonTap, width=15)
        loginBtn.grid(column=1, row=2, pady=(10, 0), sticky='w')
        registerBtn = ttk.Button(frm, text="Register", command=lambda: self.controller.showFrame(RegisterFrame),
                                 width=15)
        registerBtn.grid(column=1, row=2, pady=(10, 0), sticky='e')


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def createAccount(self):
        print(self.email.get().strip())
        if self.confirmPass.get().strip() == self.password.get().strip() and len(
                self.password.get().strip()) > 0 and len(self.email.get().strip()) > 0:
            firebaseRegister(self.email.get().strip(), self.password.get().strip(),
                             self.name.get().strip() + ' ' + self.surname.get().strip())

    def _build(self):
        pad = 10
        frm = ttk.Frame(self)
        frm.pack(padx=pad, pady=pad)

        ttk.Label(frm, text="Email:").grid(column=0, row=0, sticky='e')
        self.email = ttk.Entry(frm, width=40)
        self.email.grid(column=1, row=0)

        ttk.Label(frm, text="Name:").grid(column=0, row=1, sticky='e')
        self.name = ttk.Entry(frm, width=40)
        self.name.grid(column=1, row=1)

        ttk.Label(frm, text="Surname:").grid(column=0, row=2, sticky='e')
        self.surname = ttk.Entry(frm, width=40)
        self.surname.grid(column=1, row=2)

        ttk.Label(frm, text="Password:").grid(column=0, row=3, sticky='e')
        self.password = ttk.Entry(frm, width=40)
        self.password.grid(column=1, row=3)

        ttk.Label(frm, text="Confirm Password:").grid(column=0, row=4, sticky='e')
        self.confirmPass = ttk.Entry(frm, width=40)
        self.confirmPass.grid(column=1, row=4)

        createButton = ttk.Button(frm, text="Create account", command=self.createAccount, width=15)
        createButton.grid(column=1, row=5, pady=(10, 0), sticky='w')

        backToLoginButton = ttk.Button(frm, text="Back to login", command=lambda: self.controller.showFrame(LoginFrame),
                                       width=15)
        backToLoginButton.grid(column=1, row=5, pady=(10, 0), sticky='e')
"""
class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
"""
if __name__ == '__main__':
    app = App()
    app.mainloop()
