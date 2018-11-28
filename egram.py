import tkinter as tk #importing tkinter library
import time
import serial
import struct
import sys

name = ""

#setting up manual bytestream (115 bytes)
startByte=16
setMode=11
URL=float(120)          # Upper Rate Limit (in BPM)
LRL=float(60)           # Lower Rate Limit (in BPM)
aAmp=float(3.5)         # Atrial Pulse Amplitude (in V)
vAmp=float(3.5)         # Ventricular Pulse Amplitude (in V)
aWid=float(200)          # Atrial Pulse Width (in msec)
vWid=float(200)          # Ventricular Pulse Width (in msec)
mode=5                  # Pacemaker mode (VOO=0,VOOR=1,AOO=2,AOOR=3,VVI=4,VVIR=5,AAI=6,AAIR=7
VRP=float(100)          # Ventricular Refractory Period (in msec)
ARP=float(100)          # Atrial Refractory Period (in msec)
hyst=float(0)           # Hysteresis (no clue)
respFac=float(8)        # Reponse Factor (1-16)
MSR=float(120)          # Maximum Sensor Rate (in BPM)
actThr=float(0.5)       # Activity Threshold (Should have numbers corresponding to accelerometer values (in g) - VLow,Low,MedLow,Med,MedHigh,High,VHigh) 
rxnTim=float(3)         # Reaction time to activity (in sec) 
recTim=float(3)         # Recovery time from activity (in sec)

class WelcomeScreen:    #First window you see

    def __init__(self, master): #must define init function when you make a class, takes parameters 'master'
                           # (which is the 'master' window, the first window that appears)
        self.B_signin = tk.Button(master, text="Sign in", command=self.SignIn_Check) #Creating button, go to 'SignIn_Button' function
        self.B_signin.grid(row=4, column=2)
        self.B_signin.config(font=("Times",15, "bold"), width=7)
        self.L_uname = tk.Label(master, text="Username:", bg="white")
        self.L_uname.grid(row=2,column=1)   #creating label with text
        self.L_uname.config(font=("Times", 15, "bold", "italic"))
        self.E_uname = tk.Entry(master)    #creating entry where users enter text
        self.E_uname.grid(row=2, column=2) #placing entry in row 2 and column 2 of window
        self.E_uname.config(highlightthickness = 5)
        self.L_pass = tk.Label(master, text="Password:", bg="white")
        self.L_pass.grid(row=3,column=1)
        self.L_pass.config(font=("Times", 15, "bold", "italic"))
        self.E_pass = tk.Entry(master)
        self.E_pass.grid(row=3, column=2)
        self.E_pass.config(highlightthickness = 5)
        self.E_pass.config(show="*") #make password show up as stars not characters
        self.button2 = tk.Button(master, text="Register", command= self.Register_Instance)
        self.button2.grid(row=4, column=3)
        self.button2.config(font=("Times",15, "bold"), width=7)
        self.label = tk.Label(master, text="Welcome\nPlease sign in or register", fg="red", bg="white")
        self.label.grid(row=0,column=2)
        self.label.config(font=("Times", 20))
        master.wm_title("Pacemaker")
        #photo = tk.PhotoImage(file="heart_Rate.gif")     #This code is not required and is used for demonstration purposes during the lab (requires a local file)
        #photo.configure()
        #label = tk.Label(self.master, image=photo)
        #label.image = photo
        #label.grid(row=5, columnspan=10)
        master.geometry("500x450")
        master.configure(background="white")
        self.master = master

    def SignIn_Check(self):    #function called when SignIn_Button is pressed

        uname = tk.Entry.get(self.E_uname)  #get user entry and store in 'uname'
        pass1 = tk.Entry.get(self.E_pass)
        global name
        name = uname
        print(name)
        blank = tk.Label(self.master, text="\t\t\t\t")  #blank text to get rid of any previous text, you'll see it's use below

        try:
            f = open("Registration_File.txt", "r+")     #try to open the file if it exists
            auth = False    #initialized to false, which is default authorization until uname and pass are proven to be correct
            for lines in f: #read file line by line
                split = lines.split()   #split lines word by word, now they're stored in a list
                if split[0] == uname and split[1] == pass1: #check if user entry is the same as what is saved in the file
                    auth = True                             #authentication is verified
                    self.SignIn_Instance() #go to this function
                    break
            if auth == False:           #if username or password is incorrect
                blank.grid(row=1, column=2)
                tk.Label(self.master, text="Wrong Username or Password\nPlease try again", fg="red").grid(row=1, column=2)


        except FileNotFoundError:   #if file is not found, no users have been registered
            tk.Label(self.master, text="No users have been registered\nplease register then sign in", fg="red").grid(row=1, column=2)


    def Register_Instance(self):      #make a new window when register button is pressed and create an instance of the class 'Register_Window'
        window = tk.Toplevel()
        R_window = Register_Window(window)

    def SignIn_Instance(self):        #make a new window when sign in button is pressed and create an instance of the class 'SignIn_Window'
        self.master.wm_state('iconic')
        window = tk.Toplevel()
        SignIn_Window(window)


class Register_Window:
    def __init__(self, slave): #slave is not the master window, it's a sub-window or a slave-window

        self.slave = slave
        L_title = tk.Label(slave, text="******REGISTRATION******", fg="green")
        L_title.grid(row=0)
        L_title.configure(font=("Times", 15, "bold", "italic"))
        tk.Label(slave, text = "Enter USERNAME (Must include at least one number and be at least 6 characters)").grid(row=1)
        self.E_uname = tk.Entry(slave)
        self.E_uname.grid(row=1, column = 1)
        tk.Label(slave, text="Enter PASSWORD (Must include at least one number and be at least 6 characters").grid(row=2)
        self.E_pass1 = tk.Entry(slave)
        self.E_pass1.config(show="*")
        self.E_pass1.grid(row=2, column = 1)
        tk.Label(slave, text="Re-enter password").grid(row=3)
        self.E_pass2 = tk.Entry(slave)
        self.E_pass2.config(show="*")
        self.E_pass2.grid(row=3, column=1)
        L_button = tk.Button(slave, text="Register", fg="red", command=self.Register_Check)
        L_button.grid(row=4, column=1)
        L_button.configure(font=("Times", 15, "bold"))

    def minimize_R(self):
        self.slave.wm_state('iconic')

    def Register_Check(self):
        uname = tk.Entry.get(self.E_uname)              #initializing variables based on user entry
        pass1 = tk.Entry.get(self.E_pass1)
        pass2 = tk.Entry.get(self.E_pass2)
        blank = tk.Label(self.slave, text="\t\t\t\t\t\t\t")
        if any(char.isdigit() for char in uname) and len(uname)>=6 and pass1==pass2 and len(pass1)>=6 and any(char.isdigit() for char in pass1):      #requirements to register
            try:
                f = open("Registration_File.txt", "r+")
                count = 0
                for line in f:
                    count+=1                #entire for loop first checks if too many user are registered
                                            #then checks if username is available
                                            #if all is good, register
                if count >= 11:
                    blank.grid(row=4)
                    overflow = tk.Label(self.slave, text = "Error: Too many people registered", fg="red")
                    overflow.grid(row=4)
                else:
                    f.seek(0)
                    same = False
                    for line in f:
                        split = line.split()
                        if split[0] == uname:
                            same = True
                            blank.grid(row=4)
                            tk.Label(self.slave, text="Username is taken, try another", fg="red").grid(row=4)
                            break
                    if same == False:
                        f.close()
                        f = open("Registration_File.txt", "a+")
                        f.write("%s   %s\n" % (uname, pass1))
                        f.close()
                        blank.grid(row=4)
                        tk.Label(self.slave, text="Registration Successful!", fg="blue").grid(row=4)
                        self.slave.after(1000, self.minimize_R)

            except FileNotFoundError:
                f = open("Registration_File.txt", "a+")     #if file is not found, create the registraion file and write uname and pass to file
                f.write("Username Password\n")
                f.write("%s   %s\n" % (uname, pass1))
                f.close()
                blank.grid(row=4)
                tk.Label(self.slave, text="Registration Successful!", fg="blue").grid(row=4)
                self.slave.after(1000, self.minimize_R)
        elif pass1!=pass2:
            blank.grid(row=4)
            tk.Label(self.slave, text="Passwords are not the same, registration unsuccessful", fg="red").grid(row=4)
        elif len(uname)<6:
            blank.grid(row=4)
            tk.Label(self.slave, text="Username is too short, registration unsuccessful", fg="red").grid(row=4)
        elif len(pass1)<6:
            blank.grid(row=4)
            tk.Label(self.slave, text="Password is too short, registration unsuccessful", fg="red").grid(row=4)
        elif any(char.isdigit() for char in uname) != True:
            blank.grid(row=4)
            tk.Label(self.slave, text="No digit in username, registration unsuccessful", fg="red").grid(row=4)
        else:
            blank.grid(row=4)
            tk.Label(self.slave, text="No digit is password, registration unsuccessful", fg="red").grid(row=4)

class SignIn_Window(WelcomeScreen):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text = "Please select a pacing mode", fg ="red")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))
        tk.Label(slave, text="").grid(row=1)
        tk.Button(slave, text="AOO", fg="blue", command=self.AOO_Instance).grid(row=2, column=1)
        tk.Button(slave, text="VOO", fg="blue", command=self.VOO_Instance).grid(row=4, column=1)
        tk.Button(slave, text="AAI", fg="blue", command=self.AAI_Instance).grid(row=6, column=1)
        tk.Button(slave, text="VVI", fg="blue", command=self.VVI_Instance).grid(row=8, column=1)
        tk.Button(slave, text="VVIR", fg="blue", command=self.VVIR_Instance).grid(row=8, column=2)
        tk.Button(slave, text="AOOR", fg="blue", command=self.AOOR_Instance).grid(row=2, column=2)
        tk.Button(slave, text="AAIR", fg="blue", command=self.AAIR_Instance).grid(row=6, column=2)
        tk.Button(slave, text="VOOR", fg="blue", command=self.VOOR_Instance).grid(row=4, column=2)
        tk.Label(slave, text="").grid(row=3)
        tk.Label(slave, text="").grid(row=5)
        tk.Label(slave, text="").grid(row=7)
        tk.Label(slave, text="").grid(row=9)
        tk.Button(slave, text="Logout", fg="red", command=self.logout).grid(row=10, column=3)
    def logout(self):
        self.slave.quit()



    def LRL_Values(self): #creating list to store the allowed range of values for Lower Rate Limit
        self.values = []
        i = 30
        while i <= 45:
            self.values.append(i)
            i = i + 5
        while i <= 89:
            self.values.append(i)
            i += 1
        while i <= 175:
            self.values.append(i)
            i = i + 5
        self.default = tk.StringVar()       #declaring variable
        self.default.set(self.values[14])   #setting the nominal value (as defined in PACEMAKER document, to be displayed as a default value)

        ##all other functions do the same thing for different parameters

    def URL_Values(self):
        self.values = []
        i = 50
        while i<=175:
            self.values.append(i)
            i = i + 5
        self.default=tk.StringVar()
        self.default.set(self.values[14])

    def Amplitude(self):
        self.values = []
        for i in range(5,33):
            self.values.append(float(i)/10)
        i = 3.5
        while i<=5:
            self.values.append(i)
            i = i + 0.5
        self.default=tk.StringVar()
        self.default.set(self.values[28])

    def Width(self):
        self.values = []
        for i in range(1,20):
            self.values.append(float(i)/10)
        self.default=tk.StringVar()
        self.default.set(self.values[3])

    def Sensitivity(self):
        self.values = [0.25, 0.5, 0.75]
        i=1.0
        while i<=10.0:
            self.values.append(i)
            i = i + 0.5
        self.A_default=tk.StringVar()
        self.A_default.set(self.values[2])
        self.V_default=tk.StringVar()
        self.V_default.set(self.values[6])

    def Refractory(self):
        self.values = []
        i=150
        while i <=500:
            self.values.append(i)
            i = i + 10
        self.A_default=tk.StringVar()
        self.A_default.set(self.values[10])
        self.V_default=tk.StringVar()
        self.V_default.set(self.values[17])

    def PVARP(self):
        self.values = []
        i = 150
        while i <= 500:
            self.values.append(i)
            i = i + 10
        self.default = tk.StringVar()
        self.default.set(self.values[10])

    def Hysteresis(self):
        self.values = []
        i = 30
        while i <= 45:
            self.values.append(i)
            i = i + 5
        while i <= 89:
            self.values.append(i)
            i += 1
        while i <= 175:
            self.values.append(i)
            i = i + 5
        self.default = tk.StringVar()
        self.default.set("OFF")

    def Smoothing(self):
        self.values = []
        i=3
        while i<=21:
            self.values.append(i)
            i = i + 3
        self.values.append(25)
        self.default = tk.StringVar()
        self.default.set("OFF")

    def F_Delay(self):
        self.values = []
        i=70
        while i<=300:
            self.values.append(i)
            i = i + 10
        self.default = tk.StringVar()
        self.default.set(self.values[8])

    def D_Delay(self):
        self.values = ["OFF", "ON"]
        self.default = tk.StringVar()
        self.default.set(self.values[0])

    def PVARP_E(self):
        self.values = ["OFF"]
        i = 50
        while i<=400:
            self.values.append(i)
            i = i + 50
        self.default = tk.StringVar()
        self.default.set(self.values[0])

    def ATR_Duration(self):
        self.values = [10]
        i = 20
        while i<=80:
            self.values.append(i)
            i = i + 20
        i = 100
        while i<=2000:
            self.values.append(i)
            i = i + 100

        self.default = tk.StringVar()
        self.default.set(self.values[1])

    def ATR_Fallback_Mode(self):
        self.values = ["OFF", "ON"]

        self.default = tk.StringVar()
        self.default.set(self.values[0])

    def ATR_Fallback_Time(self):
        self.values = [1,2,3,4,5]

        self.default = tk.StringVar()
        self.default.set(self.values[0])

    def S_Delay_Offset(self):
        self.values = ["OFF"]
        i = -10
        while i>=-100:
            self.values.append(i)
            i = i - 10
        self.default = tk.StringVar()
        self.default.set(self.values[1])

    def Max_Sensor_Rate(self):
        self.values = []
        i=50
        while i<=175:
            self.values.append(i)
            i = i + 5
        self.default = tk.StringVar()
        self.default.set(self.values[14])

    def Threshold(self):
        self.values = ["V-Low", "Low", "Med-Low", "Med", "Med-High","High", "V-High"]
        self.default = tk.StringVar()
        self.default.set(self.values[3])

    def Reaction_Time(self):
        self.values = [10,20,30,40,50]

        self.default = tk.StringVar()
        self.default.set(self.values[2])

    def R_Factor(self):
        self.values = []
        i=1
        while i<=16:
            self.values.append(i)
            i = i + 1

        self.default = tk.StringVar()
        self.default.set(self.values[7])

    def Recovery_Time(self):
        self.values = []
        i = 2
        while i<=16:
            self.values.append(i)
            i = i + 1

        self.default = tk.StringVar()
        self.default.set(self.values[3])

    def AOO_Instance(self):
        window = tk.Toplevel()
        instance = AOO_Window(window)  #creating instance of AOO_Window ( see below )

    def VOO_Instance(self):
        window = tk.Toplevel()
        instance = VOO_Window(window)
        #creating instance of VOO_Window ( see below )

    def AAI_Instance(self):
        window = tk.Toplevel()
        instance = AAI_Window(window)

    def VVI_Instance(self):
        window = tk.Toplevel()
        instance = VVI_Window(window)

    def VVIR_Instance(self):
        window = tk.Toplevel()
        instance = VVIR_Window(window)

    def AOOR_Instance(self):
        window = tk.Toplevel()
        instance = AOOR_Window(window)

    def AAIR_Instance(self):
        window = tk.Toplevel()
        instance = AAIR_Window(window)

    def VOOR_Instance(self):
        window = tk.Toplevel()
        instance = VOOR_Window(window)

class serialCom:
    def send(self):
        ser = serial.Serial(
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        port = "COM7",
        baudrate=115200
        )

        global startByte
        global setMode
        global URL
        global LRL
        global aAmp
        global vAmp
        global aWid
        global vWid
        global mode
        global VRP
        global ARP
        global hyst
        global respFac
        global MSR
        global actThr
        global rxnTim
        global recTim

        print("Is Serial Port Open:",ser.isOpen())

        var=struct.pack('<BBddddddBdddddddd',startByte,setMode,URL,LRL,aAmp,vAmp,aWid,vWid,mode,VRP,ARP,hyst,respFac,MSR,actThr,rxnTim,recTim)  # B for unsigned char, takes an int 
                                                                                                                                        # d for double, takes a float
                                                                                                                                        # < for little-endian, as programmed on FRDM board thru Simulink
        print("To send (in binary): ", var)
        print("Size of string representation is {}.".format(struct.calcsize('<BBddddddBdddddddd')))
        print("To send (in decimal): ", struct.unpack('<BBddddddBdddddddd',var))


        print("send1",ser.write(var))   # struct.pack already packs into byte array in binary, so we can just send that over serial

        time.sleep(10)

        #mode=1
        #LRL=float(30)
        #actThr=float(1)

        #var=struct.pack('<BBddddddBdddddddd',startByte,setMode,URL,LRL,aAmp,vAmp,aWid,vWid,mode,VRP,ARP,hyst,respFac,MSR,actThr,rxnTim,recTim)
        #print("send2",ser.write(var))

        ser.close()
        print("Serial Port Closed")

class AOO_Window(SignIn_Window,serialCom):

    def __init__(self, slave):      #each block makes a label, calls the function that contains the appropriate list
        self.slave = slave                            #and creates a dropdown menu
        L_title = tk.Label(slave, text="Please enter parameter values for AOO pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "AOO\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[3].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[4].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)

        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=24, column=6)

        tk.Label(slave, text="\t\t\t\t").grid(row=9)
        cur_device = tk.Label(slave, text="Current pacemaker device: PACEMAKER")
        cur_device.grid(row=10, columnspan=3)
        cur_device.config(font=("Helvetica", "12", "bold", "italic", "underline"))
        comm = tk.Label(slave, text="No communication with PACEMAKER device")
        comm.grid(row=12, columnspan=3)
        comm.config(font=("Helvetica", "12", "bold", "italic", "underline"))

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        serialCom.send(self)
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("AOO\n")
        print("")

        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.close()

    def verifyMode(self):
            if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
                tk.Label(self.slave,
                text="Upper rate limit must be higher than Lower rate limit!").grid(
                row=27, column=6)
            else:
                global startByte
                global setMode
                global URL
                global LRL
                global aAmp
                global vAmp
                global aWid
                global vWid
                global mode
                mode = 2
                global VRP
                global ARP
                global hyst
                global respFac
                global MSR
                global actThr
                global rxnTim
                global recTim

                self.B_start.config(state="active")
                tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
                tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class VOO_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
            self.slave = slave
            L_title = tk.Label(slave,
                               text="Please enter parameter values for VOO pacing mode\n(Default = Nominal Value)",
                               fg="green")
            L_title.grid(row=0, columnspan=4)
            L_title.configure(font=("Times", 15, "bold", "italic"))
            fileExist = True
            wrongMode = False
            try:
                filename = name + ".txt"
                file = open(filename, "r")
            except FileNotFoundError:
                fileExist = False

            if(fileExist == True):
                array = file.readlines()
                file.close()
                if(array[0] == "VOO\n"):
                    self.LRL_Values()
                    self.O_LRL = tk.StringVar()
                    self.O_LRL.set(array[1].strip("\n"))
                    tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                    tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                    tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                    self.URL_Values()
                    self.O_URL = tk.StringVar()
                    self.O_URL.set(array[2].strip("\n"))
                    tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                    tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                    tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                    self.Amplitude()
                    self.O_Amplitude = tk.StringVar()
                    self.O_Amplitude.set(array[3].strip("\n"))
                    tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                    tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
                    tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                    self.Width()
                    self.O_Width = tk.StringVar()
                    self.O_Width.set(array[4].strip("\n"))
                    tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                    tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)
                else:
                    wrongMode = True

            if(fileExist == False or wrongMode == True):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(self.default.get())
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(self.default.get())
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(self.default.get())
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(self.default.get())
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)

            B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
            B_auth.grid(row=25, column=6)
            self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
            self.B_start.grid(row=26, column=6)
            Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
            Egram.grid(row=24, column=6)


            tk.Label(slave, text="\t\t\t\t").grid(row=9)
            cur_device = tk.Label(slave, text="Current pacemaker device: PACEMAKER")
            cur_device.grid(row=10, columnspan=3)
            cur_device.config(font=("Helvetica", "12", "bold", "italic", "underline"))
            comm = tk.Label(slave, text="No communication with PACEMAKER device")
            comm.grid(row=12, columnspan=3)
            comm.config(font=("Helvetica", "12", "bold", "italic", "underline"))

    def Egram_Window(self):
        tk.Toplevel()




    def saveSettings(self):
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("VOO\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.close()

    def verifyMode(self):

        if(int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global startByte
            global setMode
            global URL
            global LRL
            LRL = float(self.O_LRL.get())
            global aAmp
            global vAmp
            global aWid
            global vWid
            global mode
            mode = 0
            global VRP
            global ARP
            global hyst
            global respFac
            global MSR
            global actThr
            global rxnTim
            global recTim
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_vPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_vPulseWidth": float(self.O_Width.get())*100,
                "p_aPulseAmplitude": 0,
                "p_aPulseWidth": 0,
                "p_paceMode": 0,
                "p_VRP": 0,
                "p_ARP": 0,
                "p_Hysteresis": 0,
                "p_responseFactor": 0,
                "p_MSR" : 0,
                "p_activityThreshold": 0,
                "p_reactionTime": 0,
                "p_recoveryTime": 0
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class AAI_Window(SignIn_Window):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for AAI pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "AAI\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[3].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[4].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Sensitivity()
                self.O_Sensitivity = tk.StringVar()
                self.O_Sensitivity.set(array[5].strip("\n"))
                tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Refractory()
                self.O_Refractory = tk.StringVar()
                self.O_Refractory.set(array[6].strip("\n"))
                tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.PVARP()
                self.O_PVARP = tk.StringVar()
                self.O_PVARP.set(array[7].strip("\n"))
                tk.Label(slave, text="PVARP (ms)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_PVARP, *self.values).grid(row=14, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

                self.Hysteresis()
                self.O_Hysteresis = tk.StringVar()
                self.O_Hysteresis.set(array[8].strip("\n"))
                tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
                tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=16, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

                self.Smoothing()
                self.O_Smoothing = tk.StringVar()
                self.O_Smoothing.set(array[9].strip("\n"))
                tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
                tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=18, column=2)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Sensitivity()
            self.O_Sensitivity = tk.StringVar()
            self.O_Sensitivity.set(self.A_default.get())
            tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Refractory()
            self.O_Refractory = tk.StringVar()
            self.O_Refractory.set(self.A_default.get())
            tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.PVARP()
            self.O_PVARP = tk.StringVar()
            self.O_PVARP.set(self.default.get())
            tk.Label(slave, text="PVARP (ms)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_PVARP, *self.values).grid(row=14, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

            self.Hysteresis()
            self.O_Hysteresis = tk.StringVar()
            self.O_Hysteresis.set(self.default.get())
            tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
            tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=16, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

            self.Smoothing()
            self.O_Smoothing = tk.StringVar()
            self.O_Smoothing.set(self.default.get())
            tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
            tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=18, column=2)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=24, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)
        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=23, column=6)

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("AAI\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Sensitivity.get() + "\n")
        file.write(self.O_Refractory.get() + "\n")
        file.write(self.O_PVARP.get() + "\n")
        file.write(self.O_Hysteresis.get() + "\n")
        file.write(self.O_Smoothing.get() + "\n")
        file.close()

    def verifyMode(self):

        if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global startByte
            global setMode
            global URL
            global LRL
            global aAmp
            global vAmp
            global aWid
            global vWid
            global mode
            global VRP
            global ARP
            global hyst
            global respFac
            global MSR
            global actThr
            global rxnTim
            global recTim
            mode = 6
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_aPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_aPulseWidth": float(self.O_Width.get())*100,
                "p_vPulseAmplitude": 0,
                "p_vPulseWidth": 0,
                "p_paceMode": "06",
                "p_VRP": 0,
                "p_ARP": self.O_Refractory.get(),
                "p_Hysteris": self.O_Hysteresis.get(),
                "p_responseFactor": 0,
                "p_MSR" : 0,
                "p_activityThreshold": 0,
                "p_reactionTime": 0,
                "p_recoveryTime": 0
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class VVI_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for VVI pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "VVI\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[3].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[4].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Sensitivity()
                self.O_Sensitivity = tk.StringVar()
                self.O_Sensitivity.set(array[5].strip("\n"))
                tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Refractory()
                self.O_Refractory = tk.StringVar()
                self.O_Refractory.set(array[6].strip("\n"))
                tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.Hysteresis()
                self.O_Hysteresis = tk.StringVar()
                self.O_Hysteresis.set(array[7].strip("\n"))
                tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=14, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

                self.Smoothing()
                self.O_Smoothing = tk.StringVar()
                self.O_Smoothing.set(array[8].strip("\n"))
                tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
                tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=16, column=2)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Sensitivity()
            self.O_Sensitivity = tk.StringVar()
            self.O_Sensitivity.set(self.V_default.get())
            tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Refractory()
            self.O_Refractory = tk.StringVar()
            self.O_Refractory.set(self.V_default.get())
            tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.Hysteresis()
            self.O_Hysteresis = tk.StringVar()
            self.O_Hysteresis.set(self.default.get())
            tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=14, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

            self.Smoothing()
            self.O_Smoothing = tk.StringVar()
            self.O_Smoothing.set(self.default.get())
            tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
            tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=16, column=2)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)

        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=24, column=6)

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        serialCom.send(self)
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("VVI\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Sensitivity.get() + "\n")
        file.write(self.O_Refractory.get() + "\n")
        file.write(self.O_Hysteresis.get() + "\n")
        file.write(self.O_Smoothing.get() + "\n")
        file.close()

    def verifyMode(self):

        if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global startByte
            global setMode
            global URL
            global LRL
            global aAmp
            global vAmp
            global aWid
            global vWid
            global mode
            mode = 4
            global VRP
            global ARP
            global hyst
            global respFac
            global MSR
            global actThr
            global rxnTim
            global recTim
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_vPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_vPulseWidth": float(self.O_Width.get())*100,
                "p_aPulseAmplitude": 0,
                "p_aPulseWidth": 0,
                "p_paceMode": "04",
                "p_VRP": self.O_Refractory.get(),
                "p_ARP": 0,
                "p_Hysteris": self.O_Hysteresis.get(),
                "p_responseFactor": 0,
                "p_MSR" : 0,
                "p_activityThreshold": 0,
                "p_reactionTime": 0,
                "p_recoveryTime": 0
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class AOOR_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for AOOR pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "AOOR\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Max_Sensor_Rate()
                self.O_Max_Sensor_Rate = tk.StringVar()
                self.O_Max_Sensor_Rate.set(array[3].strip("\n"))
                tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[4].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[5].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Threshold()
                self.O_Threshold = tk.StringVar()
                self.O_Threshold.set(array[6].strip("\n"))
                tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.Reaction_Time()
                self.O_Reaction_Time = tk.StringVar()
                self.O_Reaction_Time.set(array[7].strip("\n"))
                tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=14, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

                self.R_Factor()
                self.O_R_Factor = tk.StringVar()
                self.O_R_Factor.set(array[8].strip("\n"))
                tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
                tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=16, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

                self.Recovery_Time()
                self.O_Recovery_Time = tk.StringVar()
                self.O_Recovery_Time.set(array[9].strip("\n"))
                tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
                tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=18, column=2)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Max_Sensor_Rate()
            self.O_Max_Sensor_Rate = tk.StringVar()
            self.O_Max_Sensor_Rate.set(self.default.get())
            tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Threshold()
            self.O_Threshold = tk.StringVar()
            self.O_Threshold.set(self.default.get())
            tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.Reaction_Time()
            self.O_Reaction_Time = tk.StringVar()
            self.O_Reaction_Time.set(self.default.get())
            tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=14, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

            self.R_Factor()
            self.O_R_Factor = tk.StringVar()
            self.O_R_Factor.set(self.default.get())
            tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
            tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=16, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

            self.Recovery_Time()
            self.O_Recovery_Time = tk.StringVar()
            self.O_Recovery_Time.set(self.default.get())
            tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
            tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=18, column=2)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)
        Egram = tk.Button(slave, text="Egram", command=self.saveSettings)
        Egram.grid(row=24, column=6)

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        serialCom.send(self)
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("AAOR\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Max_Sensor_Rate.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Threshold.get() + "\n")
        file.write(self.O_Reaction_Time.get() + "\n")
        file.write(self.O_R_Factor.get() + "\n")
        file.write(self.O_Recovery_Time.get() + "\n")
        file.close()

    def verifyMode(self):

        if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global mode
            mode = 3
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_aPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_aPulseWidth": float(self.O_Width.get())*100,
                "p_vPulseAmplitude": 0,
                "p_vPulseWidth": 0,
                "p_paceMode": "03",
                "p_VRP": 0,
                "p_ARP": 0,
                "p_Hysteris": 0,
                "p_responseFactor": self.O_R_Factor.get(),
                "p_MSR" : 60000/int(self.O_Max_Sensor_Rate.get()),
                "p_activityThreshold": self.O_Threshold.get(),
                "p_reactionTime": self.O_Reaction_Time.get(),
                "p_recoveryTime": self.O_Recovery_Time.get()
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class VOOR_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for VOOR pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "VOOR\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Max_Sensor_Rate()
                self.O_Max_Sensor_Rate = tk.StringVar()
                self.O_Max_Sensor_Rate.set(array[3].strip("\n"))
                tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[4].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[5].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Threshold()
                self.O_Threshold = tk.StringVar()
                self.O_Threshold.set(array[6].strip("\n"))
                tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.Reaction_Time()
                self.O_Reaction_Time = tk.StringVar()
                self.O_Reaction_Time.set(array[7].strip("\n"))
                tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=14, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

                self.R_Factor()
                self.O_R_Factor = tk.StringVar()
                self.O_R_Factor.set(array[8].strip("\n"))
                tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
                tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=16, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

                self.Recovery_Time()
                self.O_Recovery_Time = tk.StringVar()
                self.O_Recovery_Time.set(array[9].strip("\n"))
                tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
                tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=18, column=2)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Max_Sensor_Rate()
            self.O_Max_Sensor_Rate = tk.StringVar()
            self.O_Max_Sensor_Rate.set(self.default.get())
            tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Threshold()
            self.O_Threshold = tk.StringVar()
            self.O_Threshold.set(self.default.get())
            tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.Reaction_Time()
            self.O_Reaction_Time = tk.StringVar()
            self.O_Reaction_Time.set(self.default.get())
            tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=14, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=15)

            self.R_Factor()
            self.O_R_Factor = tk.StringVar()
            self.O_R_Factor.set(self.default.get())
            tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=16, column=0)
            tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=16, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=17)

            self.Recovery_Time()
            self.O_Recovery_Time = tk.StringVar()
            self.O_Recovery_Time.set(self.default.get())
            tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=18, column=0)
            tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=18, column=2)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)

        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=24, column=6)

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        serialCom.send(self)
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("VOOR\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Max_Sensor_Rate.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Threshold.get() + "\n")
        file.write(self.O_Reaction_Time.get() + "\n")
        file.write(self.O_R_Factor.get() + "\n")
        file.write(self.O_Recovery_Time.get() + "\n")
        file.close()

    def verifyMode(self):

        if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global mode
            mode = 0
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_vPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_vPulseWidth": float(self.O_Width.get())*100,
                "p_aPulseAmplitude": 0,
                "p_aPulseWidth": 0,
                "p_paceMode": "01",
                "p_VRP": 0,
                "p_ARP": 0,
                "p_Hysteris": 0,
                "p_responseFactor": self.O_R_Factor.get(),
                "p_MSR" : 60000/int(self.O_Max_Sensor_Rate.get()),
                "p_activityThreshold": self.O_Threshold.get(),
                "p_reactionTime": self.O_Reaction_Time.get(),
                "p_recoveryTime": self.O_Recovery_Time.get()
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27,column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)

class AAIR_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for AAIR pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "AAIR\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Max_Sensor_Rate()
                self.O_Max_Sensor_Rate = tk.StringVar()
                self.O_Max_Sensor_Rate.set(array[3].strip("\n"))
                tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[4].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[5].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Sensitivity()
                self.O_Sensitivity = tk.StringVar()
                self.O_Sensitivity.set(array[6].strip("\n"))
                tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.Refractory()
                self.O_Refractory = tk.StringVar()
                self.O_Refractory.set(array[7].strip("\n"))
                tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=14, column=2)

                self.PVARP()
                self.O_PVARP = tk.StringVar()
                self.O_PVARP.set(array[8].strip("\n"))
                tk.Label(slave, text="PVARP (ms)", font=("Helvetica", 10, "bold")).grid(row=2, column=3)
                tk.OptionMenu(slave, self.O_PVARP, *self.values).grid(row=2, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3, column=3)

                self.Hysteresis()
                self.O_Hysteresis = tk.StringVar()
                self.O_Hysteresis.set(array[9].strip("\n"))
                tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=3)
                tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=4, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5, column=3)

                self.Smoothing()
                self.O_Smoothing = tk.StringVar()
                self.O_Smoothing.set(array[10].strip("\n"))
                tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=6, column=3)
                tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=6, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7, column=3)

                self.Threshold()
                self.O_Threshold = tk.StringVar()
                self.O_Threshold.set(array[11].strip("\n"))
                tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=8, column=3)
                tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=8, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9, column=3)

                self.Reaction_Time()
                self.O_Reaction_Time = tk.StringVar()
                self.O_Reaction_Time.set(array[12].strip("\n"))
                tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=10, column=3)
                tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=10, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11, column=3)

                self.R_Factor()
                self.O_R_Factor = tk.StringVar()
                self.O_R_Factor.set(array[13].strip("\n"))
                tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=12, column=3)
                tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=12, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13, column=3)

                self.Recovery_Time()
                self.O_Recovery_Time = tk.StringVar()
                self.O_Recovery_Time.set(array[14].strip("\n"))
                tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=14, column=3)
                tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=14, column=5)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Max_Sensor_Rate()
            self.O_Max_Sensor_Rate = tk.StringVar()
            self.O_Max_Sensor_Rate.set(self.default.get())
            tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Sensitivity()
            self.O_Sensitivity = tk.StringVar()
            self.O_Sensitivity.set(self.V_default.get())
            tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.Refractory()
            self.O_Refractory = tk.StringVar()
            self.O_Refractory.set(self.V_default.get())
            tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=14, column=2)

            self.PVARP()
            self.O_PVARP = tk.StringVar()
            self.O_PVARP.set(self.default.get())
            tk.Label(slave, text="PVARP (ms)", font=("Helvetica", 10, "bold")).grid(row=2, column=3)
            tk.OptionMenu(slave, self.O_PVARP, *self.values).grid(row=2, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3, column=3)

            self.Hysteresis()
            self.O_Hysteresis = tk.StringVar()
            self.O_Hysteresis.set(self.default.get())
            tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=3)
            tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=4, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5, column=3)

            self.Smoothing()
            self.O_Smoothing = tk.StringVar()
            self.O_Smoothing.set(self.default.get())
            tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=6, column=3)
            tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=6, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7, column=3)

            self.Threshold()
            self.O_Threshold = tk.StringVar()
            tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=8, column=3)
            tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=8, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9, column=3)

            self.Reaction_Time()
            self.O_Reaction_Time = tk.StringVar()
            self.O_Reaction_Time.set(self.default.get())
            tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=10, column=3)
            tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=10, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11, column=3)

            self.R_Factor()
            self.O_R_Factor = tk.StringVar()
            self.O_R_Factor.set(self.default.get())
            tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=12, column=3)
            tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=12, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13, column=3)

            self.Recovery_Time()
            self.O_Recovery_Time = tk.StringVar()
            self.O_Recovery_Time.set(self.default.get())
            tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=14, column=3)
            tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=14, column=5)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)
        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=24, column=6)

    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("AAOR\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Max_Sensor_Rate.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Sensitivity.get() + "\n")
        file.write(self.O_Refractory.get() + "\n")
        file.write(self.O_PVARP.get() + "\n")
        file.write(self.O_Hysteresis.get() + "\n")
        file.write(self.O_Smoothing.get() + "\n")
        file.write(self.O_Threshold.get() + "\n")
        file.write(self.O_Reaction_Time.get() + "\n")
        file.write(self.O_R_Factor.get() + "\n")
        file.write(self.O_Recovery_Time.get() + "\n")
        file.close()

    def verifyMode(self):

        if (int(self.O_LRL.get()) >= int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global mode
            mode = 7
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_aPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_aPulseWidth": float(self.O_Width.get())*100,
                "p_vPulseAmplitude": 0,
                "p_vPulseWidth": 0,
                "p_paceMode": "07",
                "p_VRP": 0,
                "p_ARP": 0,
                "p_Hysteris": self.O_Hysteresis.get(),
                "p_responseFactor": self.O_R_Factor.get(),
                "p_MSR" : 60000/int(self.O_Max_Sensor_Rate.get()),
                #"p_activityThreshold": self.O_Threshold.get(),
                "p_reactionTime": self.O_Reaction_Time.get(),
                "p_recoveryTime": self.O_Recovery_Time.get()
            }
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)


class VVIR_Window(SignIn_Window,serialCom):

    def __init__(self, slave):
        self.slave = slave
        L_title = tk.Label(slave, text="Please enter parameter values for VVIR pacing mode\n(Default = Nominal Value)", fg="green")
        L_title.grid(row=0, columnspan=4)
        L_title.configure(font=("Times", 15, "bold", "italic"))

        fileExist = True
        wrongMode = False
        try:
            filename = name + ".txt"
            file = open(filename, "r")
        except FileNotFoundError:
            fileExist = False

        if (fileExist == True):
            array = file.readlines()
            file.close()
            if (array[0] == "VVIR\n"):
                self.LRL_Values()
                self.O_LRL = tk.StringVar()
                self.O_LRL.set(array[1].strip("\n"))
                tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
                tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

                self.URL_Values()
                self.O_URL = tk.StringVar()
                self.O_URL.set(array[2].strip("\n"))
                tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
                tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

                self.Max_Sensor_Rate()
                self.O_Max_Sensor_Rate = tk.StringVar()
                self.O_Max_Sensor_Rate.set(array[3].strip("\n"))
                tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
                tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

                self.Amplitude()
                self.O_Amplitude = tk.StringVar()
                self.O_Amplitude.set(array[4].strip("\n"))
                tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
                tk.OptionMenu(slave, self.O_Amplitude, "OFF", *self.values).grid(row=8, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

                self.Width()
                self.O_Width = tk.StringVar()
                self.O_Width.set(array[5].strip("\n"))
                tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
                tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

                self.Sensitivity()
                self.O_Sensitivity = tk.StringVar()
                self.O_Sensitivity.set(array[6].strip("\n"))
                tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
                tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=12, column=2)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

                self.Recovery_Time()
                self.O_Recovery_Time = tk.StringVar()
                self.O_Recovery_Time.set(array[7].strip("\n"))
                tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
                tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=14, column=2)

                self.Refractory()
                self.O_Refractory = tk.StringVar()
                self.O_Refractory.set(array[8].strip("\n"))
                tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=2, column=3)
                tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=2, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=3, column=3)

                self.Hysteresis()
                self.O_Hysteresis = tk.StringVar()
                self.O_Hysteresis.set(array[9].strip("\n"))
                tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=3)
                tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=4, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=5, column=3)

                self.Smoothing()
                self.O_Smoothing = tk.StringVar()
                self.O_Smoothing.set(array[10].strip("\n"))
                tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=6, column=3)
                tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=6, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=7, column=3)

                self.Threshold()
                self.O_Threshold = tk.StringVar()
                self.O_Threshold.set(array[11].strip("\n"))
                tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=8, column=3)
                tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=8, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=9, column=3)

                self.Reaction_Time()
                self.O_Reaction_Time = tk.StringVar()
                self.O_Reaction_Time.set(array[12].strip("\n"))
                tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=10, column=3)
                tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=10, column=5)
                tk.Frame(slave, height=1, width=400, bg="green").grid(row=11, column=3)

                self.R_Factor()
                self.O_R_Factor = tk.StringVar()
                self.O_R_Factor.set(array[13].strip("\n"))
                tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=12, column=3)
                tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=12, column=5)

            else:
                wrongMode = True
        if (fileExist == False or wrongMode == True):
            self.LRL_Values()
            self.O_LRL = tk.StringVar()
            self.O_LRL.set(self.default.get())
            tk.Label(slave, text="Lower Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=2, column=0)
            tk.OptionMenu(slave, self.O_LRL, *self.values).grid(row=2, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3)

            self.URL_Values()
            self.O_URL = tk.StringVar()
            self.O_URL.set(self.default.get())
            tk.Label(slave, text="Upper Rate Limit (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=0)
            tk.OptionMenu(slave, self.O_URL, *self.values).grid(row=4, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5)

            self.Max_Sensor_Rate()
            self.O_Max_Sensor_Rate = tk.StringVar()
            self.O_Max_Sensor_Rate.set(self.default.get())
            tk.Label(slave, text="Maximum Sensor Rate (PPM)", font=("Helvetica", 10, "bold")).grid(row=6, column=0)
            tk.OptionMenu(slave, self.O_Max_Sensor_Rate, *self.values).grid(row=6, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7)

            self.Amplitude()
            self.O_Amplitude = tk.StringVar()
            self.O_Amplitude.set(self.default.get())
            tk.Label(slave, text="Amplitude (V)", font=("Helvetica", 10, "bold")).grid(row=8, column=0)
            tk.OptionMenu(slave, self.O_Amplitude, 0, *self.values).grid(row=8, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9)

            self.Width()
            self.O_Width = tk.StringVar()
            self.O_Width.set(self.default.get())
            tk.Label(slave, text="Width (ms)", font=("Helvetica", 10, "bold")).grid(row=10, column=0)
            tk.OptionMenu(slave, self.O_Width, "0.05", *self.values).grid(row=10, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11)

            self.Sensitivity()
            self.O_Sensitivity = tk.StringVar()
            self.O_Sensitivity.set(self.V_default.get())
            tk.Label(slave, text="Sensitivity (mV)", font=("Helvetica", 10, "bold")).grid(row=12, column=0)
            tk.OptionMenu(slave, self.O_Sensitivity, *self.values).grid(row=12, column=2)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=13)

            self.Recovery_Time()
            self.O_Recovery_Time = tk.StringVar()
            self.O_Recovery_Time.set(self.default.get())
            tk.Label(slave, text="Recovery Time (min)", font=("Helvetica", 10, "bold")).grid(row=14, column=0)
            tk.OptionMenu(slave, self.O_Recovery_Time, *self.values).grid(row=14, column=2)

            self.Refractory()
            self.O_Refractory = tk.StringVar()
            self.O_Refractory.set(self.V_default.get())
            tk.Label(slave, text="Refractory Period (ms)", font=("Helvetica", 10, "bold")).grid(row=2, column=3)
            tk.OptionMenu(slave, self.O_Refractory, *self.values).grid(row=2, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=3, column=3)

            self.Hysteresis()
            self.O_Hysteresis = tk.StringVar()
            self.O_Hysteresis.set(self.default.get())
            tk.Label(slave, text="Hysteresis (PPM)", font=("Helvetica", 10, "bold")).grid(row=4, column=3)
            tk.OptionMenu(slave, self.O_Hysteresis, "OFF", *self.values).grid(row=4, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=5, column=3)

            self.Smoothing()
            self.O_Smoothing = tk.StringVar()
            self.O_Smoothing.set(self.default.get())
            tk.Label(slave, text="Rate Smoothing (%)", font=("Helvetica", 10, "bold")).grid(row=6, column=3)
            tk.OptionMenu(slave, self.O_Smoothing, "OFF", *self.values).grid(row=6, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=7, column=3)

            self.Threshold()
            self.O_Threshold = tk.StringVar()
            self.O_Threshold.set(self.default.get())
            tk.Label(slave, text="Activity Threshold", font=("Helvetica", 10, "bold")).grid(row=8, column=3)
            tk.OptionMenu(slave, self.O_Threshold, *self.values).grid(row=8, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=9, column=3)

            self.Reaction_Time()
            self.O_Reaction_Time = tk.StringVar()
            self.O_Reaction_Time.set(self.default.get())
            tk.Label(slave, text="Reaction Time (sec)", font=("Helvetica", 10, "bold")).grid(row=10, column=3)
            tk.OptionMenu(slave, self.O_Reaction_Time, *self.values).grid(row=10, column=5)
            tk.Frame(slave, height=1, width=400, bg="green").grid(row=11, column=3)

            self.R_Factor()
            self.O_R_Factor = tk.StringVar()
            self.O_R_Factor.set(self.default.get())
            tk.Label(slave, text="Response Factor", font=("Helvetica", 10, "bold")).grid(row=12, column=3)
            tk.OptionMenu(slave, self.O_R_Factor, *self.values).grid(row=12, column=5)

        B_auth = tk.Button(slave, text="Verify", command=self.verifyMode)
        B_auth.grid(row=25, column=6)
        self.B_start = tk.Button(slave, text="Start Mode", state="disabled", command=self.saveSettings)
        self.B_start.grid(row=26, column=6)
        Egram = tk.Button(slave, text="Egram", command=self.Egram_Window)
        Egram.grid(row=24, column=6)


    def Egram_Window(self):
        tk.Toplevel()

    def saveSettings(self):
        serialCom.send(self)
        fileName = name + ".txt"
        file = open(fileName, "w")
        file.write("AAOR\n")
        file.write(self.O_LRL.get() + "\n")
        file.write(self.O_URL.get() + "\n")
        file.write(self.O_Max_Sensor_Rate.get() + "\n")
        file.write(self.O_Amplitude.get() + "\n")
        file.write(self.O_Width.get() + "\n")
        file.write(self.O_Sensitivity.get() + "\n")
        file.write(self.O_Recovery_Time.get() + "\n")
        file.write(self.O_Refractory.get() + "\n")
        file.write(self.O_Hysteresis.get() + "\n")
        file.write(self.O_Smoothing.get() + "\n")
        file.write(self.O_Threshold.get() + "\n")
        file.write(self.O_Reaction_Time.get() + "\n")
        file.write(self.O_R_Factor.get() + "\n")
        file.close()
     

    def verifyMode(self):

        if (int(self.O_LRL.get()) > int(self.O_URL.get())):
            tk.Label(self.slave, text="Upper rate limit must be higher than Lower rate limit!").grid(row=27, column=6)
        else:
            global mode
            mode = 5
            store = {
                "p_LRL": 60000/int(self.O_LRL.get()),
                "p_URL": 60000/int(self.O_URL.get()),
                "p_vPulseAmplitude": float(self.O_Amplitude.get())*10,
                "p_vPulseWidth": float(self.O_Width.get())*100,
                "p_aPulseAmplitude": 0,
                "p_aPulseWidth": 0,
                "p_paceMode": "05",
                "p_VRP": 0,
                "p_ARP": 0,
                "p_Hysteris": self.O_Hysteresis.get(),
                "p_responseFactor": self.O_R_Factor.get(),
                "p_MSR" : 60000/int(self.O_Max_Sensor_Rate.get()),
                "p_activityThreshold": self.O_Threshold.get(),
                "p_reactionTime": self.O_Reaction_Time.get(),
                "p_recoveryTime": self.O_Recovery_Time.get()
            }
            print(store["p_MSR"])
            self.B_start.config(state="active")
            tk.Label(self.slave, text="\t\t\t\t").grid(row=27, column=6)
            tk.Label(self.slave, text="Verification Successful").grid(row=27, column=6)




def main():
    master = tk.Tk()
    x = WelcomeScreen(master)
    master.mainloop()

main()
