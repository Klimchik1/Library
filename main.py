import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from cachetools.func import ttl_cache
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
        self.geometry('1000x700')
        self.resizable(True, True)

        self.buildFrames()
        self.showFrame(LoginFrame)

    def buildFrames(self):
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame, LoanHistoryFrame, BookManagerFrame, SearchFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def showFrame(self, frameClass):
        frame = self.frames[frameClass]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()
    def login(self):
        self.showFrame(DashboardFrame)
    def logout(self):
        pass


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def loginButtonTap(self):
        email = self.email.get().strip()
        password = self.password.get().strip()

        if len(email) > 0 and len(password) > 0:
            self.controller.login()



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

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill='x', pady=8)
        self.welcomeLabel=ttk.Label(top, text="Welcome")
        self.welcomeLabel.pack(side='left', padx=8)
        ttk.Button(top, text='Logout', command=self.controller.logout).pack(side='right', padx=8)
        ttk.Button(top, text='Manage Books', command=lambda: self.controller.showFrame(BookManagerFrame)).pack(side='right', padx=8)
        ttk.Button(top, text='Search', command=lambda: self.controller.showFrame(SearchFrame)).pack(side='right', padx=8)
        ttk.Button(top, text='My Loans', command=lambda: self.controller.showFrame(LoanHistoryFrame)).pack(side='right', padx=8)


        mid = ttk.Frame(self)
        mid.pack(fill='both', expand=True, padx=8, pady=8)
        summaryLabel = ttk.LabelFrame(mid, text="Summary")
        summaryLabel.pack(fill='x', pady=8)
        self.borrowedLabel=ttk.Label(summaryLabel, text="Currently Borrowed: 0")
        self.borrowedLabel.pack(side='left', padx=8, pady=8)
        self.refreshButton=ttk.Button(summaryLabel, text="Refresh", command=self.on_show)
        self.refreshButton.pack(side='right', padx=8)
        loansLabel = ttk.LabelFrame(mid, text="Active loans (soonest due first")
        loansLabel.pack(fill='x', pady=8)
        self.loansTree=ttk.Treeview(loansLabel, show='headings', columns=["title", "user", "due"])
        self.loansTree.heading('title', text='Title')
        self.loansTree.heading('user', text='User')
        self.loansTree.heading('due', text='Due')
        self.loansTree.pack(fill='both', expand=True)


    def on_show(self):
        pass

class BookManagerFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill='x', pady=8)
        ttk.Button(top, text='Back', command=lambda: self.controller.showFrame(DashboardFrame)).pack(side='left',                                                                                         padx=8)
        ttk.Button(top, text='Add Book', command=self.add_book).pack(side='left')
        ttk.Button(top, text='Edit Selected', command=self.edit_selected).pack(side='left')
        ttk.Button(top, text='Delete Selected', command=self.delete_selected).pack(side='left')
        ttk.Button(top, text='Borrow Selected', command=self.borrow_selected).pack(side='left')
        ttk.Button(top, text='Return Selected Loan', command=self.return_selected_loan).pack(side='left')

        mid = ttk.Frame(self)
        mid.pack(fill='both', expand=True, padx=8, pady=8)
        self.loansTree = ttk.Treeview(mid, show='headings', columns=["title", "author", "genre", "available", "total"])
        self.loansTree.heading('title', text='Title')
        self.loansTree.heading('author', text='Author')
        self.loansTree.heading('genre', text='Genre')
        self.loansTree.heading('available', text='Available')
        self.loansTree.heading('total', text='Total')
        self.loansTree.pack(fill='both', expand=True)


        bottom = ttk.Frame(self)
        bottom.pack(fill='x', pady=8)
        ttk.Button(bottom, text='Refresh', command=lambda: self.on_show).pack(side='left', padx=8)

    def add_book(self):
        dlg=AddBookFrame(self, 'Add Book')
        self.wait_window(dlg)
    def edit_selected(self):
        pass
    def delete_selected(self):
        pass
    def borrow_selected(self):
        pass
    def return_selected_loan(self):
        pass

class AddBookFrame(tk.Toplevel):
    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.initial = initial
        self.result = None
        self._build()

    def _build(self):
        pad = 10
        frm = ttk.Frame(self)
        frm.pack(padx=pad, pady=pad)

        ttk.Label(frm, text="Title").grid(column=0, row=0, sticky='e')
        self.f_title = ttk.Entry(frm, width=40)
        self.f_title.grid(column=1, row=0)

        ttk.Label(frm, text="Author").grid(column=0, row=1, sticky='e')
        self.f_author = ttk.Entry(frm, width=40)
        self.f_author.grid(column=1, row=1)

        ttk.Label(frm, text="Genre").grid(column=0, row=2, sticky='e')
        self.f_genre = ttk.Entry(frm, width=40)
        self.f_genre.grid(column=1, row=2)

        ttk.Label(frm, text="ISBN").grid(column=0, row=3, sticky='e')
        self.f_isbn = ttk.Entry(frm, width=40)
        self.f_isbn.grid(column=1, row=3)

        ttk.Label(frm, text="Copies").grid(column=0, row=4, sticky='e')
        self.f_copies = ttk.Entry(frm, width=40)
        self.f_copies.grid(column=1, row=4)

        saveButton = ttk.Button(frm, text="Save", command=self.save, width=15)
        saveButton.grid(column=1, row=5, pady=(10, 0), sticky='w')

        cancelButton = ttk.Button(frm, text="Cancel", command=self.destroy, width=15)
        cancelButton.grid(column=1, row=5, pady=(10, 0), sticky='e')

    def save(self):
        pass

class SearchFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill='x', pady=8)
        ttk.Button(top, text='Back', command=lambda: self.controller.showFrame(DashboardFrame)).pack(side='left', padx=8)
        ttk.Label(top, text='Title').pack(side='left')
        self.s_title = ttk.Entry(top, width=25).pack(side='left')
        ttk.Label(top, text='Author').pack(side='left')
        self.s_author = ttk.Entry(top, width=25).pack(side='left')
        ttk.Label(top, text='Genre').pack(side='left')
        self.s_genre = ttk.Entry(top, width=25).pack(side='left')
        ttk.Button(top, text='Search', command=self.search).pack(side='left')

        mid = ttk.Frame(self)
        mid.pack(fill='both', expand=True, padx=8, pady=8)
        self.loansTree = ttk.Treeview(mid, show='headings', columns=["title", "author", "genre", "available"])
        self.loansTree.heading('title', text='Title')
        self.loansTree.heading('author', text='Author')
        self.loansTree.heading('genre', text='Genre')
        self.loansTree.heading('available', text='Available')
        self.loansTree.pack(fill='both', expand=True)


        bottom = ttk.Frame(self)
        bottom.pack(fill='x', pady=8)
        ttk.Button(bottom, text='Borrow Selected', command=lambda: self.borrow_selected).pack(side='left', padx=8)

    def search(self):
        pass
    def borrow_selected(self):
        pass
class LoanHistoryFrame(ttk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill='x', pady=8)

        ttk.Button(top, text='Back', command=lambda: self.controller.showFrame(DashboardFrame)).pack(side='left', padx=8)
        ttk.Button(top, text='Refresh', command=self.on_show).pack(side='left', padx=8)

        mid = ttk.Frame(self)
        mid.pack(fill='both', expand=True, padx=8, pady=8)
        self.loansTree = ttk.Treeview(mid, show='headings', columns=["title", "borrowed_at", "returned_at"])
        self.loansTree.heading('title', text='Title')
        self.loansTree.heading('borrowed_at', text='Borrowed at')
        self.loansTree.heading('returned_at', text='Returned at')
        self.loansTree.pack(fill='both', expand=True)

        bottom = ttk.Frame(self)
        bottom.pack(fill='x', pady=8)
        ttk.Button(bottom, text='Return selected', command=lambda: self.return_selected).pack(side='left', padx=8)


    def on_show(self):
        pass

    def return_selected(self):
        pass


if __name__ == '__main__':
    app = App()
    app.mainloop()
