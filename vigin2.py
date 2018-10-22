import Tkinter as tk


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        window = tk.Frame(self)

        window.pack(side="top", fill="both", expand=True)

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginScreen, SignupScreen, Home):
            frame = F(window, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, wind):
        frame = self.frames[wind]
        frame.tkraise()


class LoginScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        file = open("rememberME.txt", "r")
        name = file.read()
        file.close()

        self.E_name = tk.Entry(self)
        if (file != ""):
            self.E_name.insert(0, name)

        L_name = tk.Label(self, text="Name")
        L_password = tk.Label(self, text="Password")

        self.E_password = tk.Entry(self)
        B_login = tk.Button(self, text="Login", command=self.auth_login)
        B_signup = tk.Button(self, text="Signup", command=lambda : controller.show_frame(SignupScreen))
        self.box_status = tk.IntVar()
        self.B_remember = tk.Checkbutton(self, text="Remember me", variable= self.box_status)

        L_name.grid(row=0, column=0)
        L_password.grid(row=1, column=0)
        self.E_name.grid(row=0, column=1)
        self.E_password.grid(row=1, column=1)
        B_login.grid(row=2,column=1)
        B_signup.grid(row=2, column=2)
        self.B_remember.grid(row=3)


    def auth_login(self):
        authName = self.E_name.get() + "," + self.E_password.get() + "\n"
        file = open("logins", "r")
        x = file.readlines()
        print(x)
        file.close()
        auth = False
        for i in x:
            if(i == authName):
                auth = True
        if(auth == False):
            L_wrongLogin = tk.Label(self, text= "Wrong username or password, Please try again")
            L_wrongLogin.grid(row=4)
        else:
            remember_status = self.box_status.get()
            if(remember_status == 1):
                file = open("rememberME.txt", "w")
                file.write(self.E_name.get())
                file.close()
            else:
                file = open("rememberME", "w")
                file.write("")
                file.close()
            self.controller.show_frame(Home)


class SignupScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.L_name = tk.Label(self, text = "Name")
        self.L_password = tk.Label(self, text="Password")
        self.L_password2 = tk.Label(self, text="Confirm Password")
        self.E_name = tk.Entry(self)
        self.E_password = tk.Entry(self)
        self.E_password2 = tk.Entry(self)
        self.B_login = tk.Button(self, text="Register", command = self.check)

        self.L_name.grid(row=0)
        self.L_password.grid(row=1)
        self.L_password2.grid(row=2)
        self.E_name.grid(row =0, column=1)
        self.E_password.grid(row=1, column=1)
        self.E_password2.grid(row=2, column=1)
        self.B_login.grid(row=3, column=1)

    def save_user(self):
        file = open("logins", "a")
        file.write(self.E_name.get() + "," + self.E_password.get() + "\n")
        file.close()

    def check(self):
        name = self.E_name.get()
        password = self.E_password.get()
        password2 = self.E_password2.get()
        print(len(name))
        print(len(password))
        if(len(name)<3):
            test2 = tk.Label(self, text="username too short")
            test2.grid(row=5)
        else:
            if(password != password2):
                test = tk.Label(self, text="Passwords do not match")
                test.grid(row=5)
            else:
                if(len(password) < 6):
                    test3 = tk.Label(self, text="not long enough password")
                    test3.grid(row=5)
                else:
                    self.save_user()
                    self.controller.show_frame(Home)


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        L_welcome = tk.Label(self, text="")
        L_welcome.pack()


app = Main()
app.mainloop()