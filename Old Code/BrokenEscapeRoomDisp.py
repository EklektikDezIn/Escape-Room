#============================================
# author: Micah Richards
# date: 10/4/17
# class: Library Work
#
# purpose: Display victory message on proper USB insertion
# input:  - USB
#         -
# output: - Victory Splash Screen
#	  -
#
#============================================

# imports
import os, pyudev, threading, time, ttk
import Tkinter as tk
from PIL import ImageTk, Image

# define global constants and Booleans
cont = False
context = pyudev.Context()
debug = True
global InDrive
InDrive = 0
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
passfile = open('passwords.txt', 'r')
password = passfile.readline().strip()

image1 = Image.open("Background Start.jpg")
image1 = image1.resize((1024, 768), Image.ANTIALIAS)

image2 = Image.open("Background Password.jpg")
image2 = image2.resize((1024, 768), Image.ANTIALIAS)

image3 = Image.open("Background USB.jpg")
image3 = image3.resize((1024, 768), Image.ANTIALIAS)

image4 = Image.open("Background Success.jpg")
image4 = image4.resize((1024, 768), Image.ANTIALIAS)

# define functions
def calctdiff(Stt, Fnt):
    if (debug):
         print('    In calctdiff()')
    Total=Fnt-Stt
    if (debug):
	print('        The total time is %f' % Total)
    Minutes = int(Total/60)
    if (debug):
	print('        The total number of minutes is %d' % Minutes)
    Seconds = int(Total % 60 )
    if (debug):
	print('        The total number of seconds  is %d' % Seconds)
    return ('%02d:%02d' % (Minutes, Seconds))

def donoth():
    pass

# ===== GUI =====
class Application (tk.Frame):

    def clearPage(self):
	if (debug):
	    print('    In clearPage()')

	for child in self.winfo_children():
	    child.grid_forget()
	if (debug):
	    print('        Page Cleared')

    def pollfordrive(self):
        if (debug):
            print('    In pollfordrive()')

        for device in iter(monitor.poll, None):
            if device.action =='add':
	        if (debug):
	            print('        You have plugged a device into the computer')
                    print('        {} connected'.format(device))
	        self.moveBar()
            if device.action =='remove':
                if (debug):
	            print('        You have unplugged a device from the computer')
                    print('        {} disconnected'.format(device))
		self.destroy()

    def __init__(self, master=None):
	tk.Frame.__init__(self, master)
	self.grid()
	self.focus()
	self.start()
	if (debug):
	    ignvar = os.system ('clear')
	    print('System initialized:')

    def start(self):
 	if (debug):
	    print('On Start Page')
	self.clearPage()

	photo_image1 = ImageTk.PhotoImage(image1)
	self.label = tk.Label(self, image = photo_image1)
	self.label.image = photo_image1
	self.label.grid()
 	if (debug):
	    print('    Background Set to \'Background Start.jpg\'')

	self.startButton = tk.Button(self, text='Start',
			             command=self.password,
				     width = 10,
				     height= 3
				     )
	self.startButton.place(x=250, y=400)
 	if (debug):
	    print('    Button StartButton Placed')

    def password(self):
	if (debug):
	    print('On Password Page')
	self.startTime = time.time()
	if (debug):
	    print('    Timer Started at %f' % self.startTime)
	self.clearPage()

	photo_image2 = ImageTk.PhotoImage(image2)
	self.label = tk.Label(self, image = photo_image2)
	self.label.image = photo_image2
	self.label.grid()
 	if (debug):
	    print('    Background Set to \'Background Password.jpg\'')

	self.passwd = tk.StringVar()
	self.PasswordPrompt = tk.Entry(self, state = tk.NORMAL, textvariable = self.passwd)
	self.PasswordPrompt.place (x=420, y=405)
	self.PasswordPrompt.focus_set()
 	if (debug):
	    print('    Entry PasswordPrompt Placed')

	self.passButton = tk.Button(self, text='Go',
			             command=self.checkPass,
				     width = 1,
				     height= 1
				     )
	self.passButton.place(x=580, y=406)
 	if (debug):
	    print('    Button passButton Placed')

    def checkPass(self):
	if (debug):
	    print ('In checkPass()')
            print ('    The entered password is: %s' % self.PasswordPrompt.get())
        if (self.PasswordPrompt.get() == password):
            if (debug):
                print ('        That is the correct password!')
	    self.USB()
        else:
            if (debug):
                print ('        That is not the correct password')
		print ('	The correct password is %s.' % password)

    def USB(self):
	if (debug):
	    print('On USB Page')
	self.clearPage()
	photo_image3 = ImageTk.PhotoImage(image3)
	self.label = tk.Label(self, image = photo_image3)
	self.label.image = photo_image3
	self.label.grid()
 	if (debug):
	    print('    Background Set to \'Background USB.jpg\'')

	self.UpLoader = ttk.Progressbar(self, length = 400, mode = 'determinate', orient = tk.HORIZONTAL)
	self.UpLoader.place(x=312, y=484)
 	if (debug):
	    print('    Progressbar UpLoader Placed')
	    print('    Waiting for Drive:')
	threading.Thread(target = self.pollfordrive).start()

    def moveBar(self):
	for i in range(0,100):
# 	    if (debug):
#	        print('    Increment UpLoader 1')
	    self.UpLoader.step()
	    self.UpLoader.after(30, donoth())
	self.Success()

    def Success(self):
	if (debug):
	    print('On Success Page')
	self.clearPage()

	photo_image4 = ImageTk.PhotoImage(image4)
	self.label = tk.Label(self, image = photo_image4)
	self.label.image = photo_image4
	self.label.grid()
 	if (debug):
	    print('    Background Set to \'Background Success.jpg\'')

	self.WinLabel = tk.Label(self, text = 'It took you %s to complete this!' % calctdiff(self.startTime, time.time()))
	self.WinLabel.place(x=220, y=400)
 	if (debug):
	    print('    Waiting for Drive:')
	threading.Thread(target = self.pollfordrive).start()
# ===== Main Program =====
app = Application()
app.master.title('RG\'s Race')
w_0, h_0 = app.master.winfo_screenwidth(), app.master.winfo_screenheight()
app.master.geometry('%dx%d+0+0' % (w_0, h_0))
#app.master.wm_attributes('-type', 'splash')
#app.master.protocol("WM_DELETE_WINDOW", dontDeleteWindow)
app.master.wm_attributes('-topmost', 'True')
app.mainloop()
#while(True):
#    cont = False
#    if (debug):
#        print ('DEBUG: The password is: %s' % password)
#
#    raw_input('Press enter to continue...')
#    startTime=time.time()
#    if (debug):
#        print ('DEBUG: The starting time is: %f' % startTime)
#
#    print ('Please insert the flashdrive with the file')
#    while (pollfordrive() != 1):
#        donoth()
#    print ('You did it!')
#    print ('Resetting System...')
#    time.sleep(1)

# End of Program
print ('\n-----End of Program-----\n')
