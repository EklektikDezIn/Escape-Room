################# EscapeRoomDisp ################################
# Eklektik Design
# Micah Richards
# 04/10/17
#           
#################################################################


################### Libraries ###################################
import os, pyudev, threading, time, ttk
import Tkinter as tk
from PIL import ImageTk, Image


################### Variables ###################################
context = pyudev.Context()								## Set context for USB monitoring
debug = True											## Set for debug terminal output
global InDrive											## Track if USB Drive is inserted
InDrive = 0												
global canUSBfile										## Check if the system can respond to USB events
canUSBfile = 0											
global moveBarcount										## Track progress for progressbar incrementing
moveBarcount = 0										
monitor = pyudev.Monitor.from_netlink(context)			## Create monitor for USB
monitor.filter_by(subsystem='usb')						
passfile = open('passwords.txt', 'r')					## Store the password for later comparison
password = passfile.readline().strip()					

image1 = Image.open("Background Start.jpg")				## Store Success page image
image1 = image1.resize((1024, 768), Image.ANTIALIAS)

image2 = Image.open("Background Password.jpg")			## Store Success page image
image2 = image2.resize((1024, 768), Image.ANTIALIAS)

image3 = Image.open("Background USB.jpg")				## Store Success page image
image3 = image3.resize((1024, 768), Image.ANTIALIAS)

image4 = Image.open("Background Success.jpg")			## Store Success page image
image4 = image4.resize((1024, 768), Image.ANTIALIAS)	


################### Functions ###################################

################### calctdiff ###################################
# Purpose: Converts a number of seconds into a formatted time
#           string
#
# Inputs:  int - start time
#		   int - finish time
# 	   
# Outputs: String - format mm:ss
#          
#################################################################
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
	
################### donoth ######################################
# Purpose: Allows blank loops
#          
# Inputs:  None
# 	   
# Outputs: None
#          
#################################################################
def donoth():
    pass

################### dontDeleteWindow ############################
# Purpose: Redirects close button function
#          
# Inputs:  None
# 	   
# Outputs: Writes 'No' to command line
#          
#################################################################
def dontDeleteWindow():
    print('No.')


################### Application #################################
class Application (tk.Frame):

	################### clearPage ###################################
	# Purpose: Removes all GUI items for page switch
	#          
	# Inputs:  Application - self
	# 	   
	# Outputs: None
	#          
	#################################################################
    def clearPage(self):
	if (debug):
	    print('    In clearPage()')

	for child in self.winfo_children():
	    child.grid_forget()
	if (debug):
	    print('        Page Cleared')
		
	################### pollfordrive ################################
	# Purpose: Recursively checks if a flashdrive has been inserted
	#           or removed and sets flags accordingly
	#
	# Inputs:  Application - self
	# 	   
	# Outputs: None
	#          
	#################################################################
    def pollfordrive(self):
	global USBfile
        if (debug):
            print('    In pollfordrive()')
	USBfile = 0
        for device in iter(monitor.poll, None):
            if device.action =='add':
	        if (debug):
	            print('        You have plugged a device into the computer')
                    print('        {} connected'.format(device))
		USBfile = 1
            if device.action =='remove':
                if (debug):
	            print('        You have unplugged a device from the computer')
                    print('        {} disconnected'.format(device))
		USBfile = 2
		
	################### checkUSBs ###################################
	# Purpose: Reads USB inserted/removed flags and runs appropriate
	#           functions
	#
	# Inputs:  Application - self
	# 	   
	# Outputs: None
	#          
	#################################################################
    def checkUSBs(self):
	global USBfile
	global canUSBfile
	if (canUSBfile == 1):
	    if (USBfile == 1):
	        USBfile = 0
	        canUSBfile = 0
	        self.moveBar()
	    elif (USBfile == 2):
	        USBfile = 0
	        canUSBfile = 0
	        self.start()
	self.after(300, self.checkUSBs)

	################### __init__ ####################################
	# Purpose: Initializes application and starts necessary
	#           subprocesses
	#
	# Inputs:  Application - self
	# 	   
	# Outputs: None
	#          
	#################################################################
    def __init__(self, master=None):
	tk.Frame.__init__(self, master)
	self.grid()
	self.focus()
	self.start()
	self.after(300, self.checkUSBs)
	threading.Thread(target = self.pollfordrive).start()
	if (debug):
	    ignvar = os.system ('clear')
	    print('System initialized:')

	################### start #######################################
	# Purpose: Displays the start page 
	#
	# Inputs Code:  Application - self
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   Button - Start
	#
	# Outputs GUI:  Advance to password page
	#################################################################
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
		
	################### password ####################################
	# Purpose: Displays the password page
	#          
	# Inputs Code:  Application - self
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   Textbox - password input
	#				Button  - checks password and advances to 
    #						   checkpass if password is correct
	#
	# Outputs GUI:  Advance to checkpass
	#          
	#################################################################
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

	################### checkPass ###################################
	# Purpose: Checks if input password matches the stored password
	#          
	# Inputs Code:  Application - self
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   None
	#
	# Outputs GUI:  Advance to USB page
	#
	#################################################################
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

	################### USB #########################################
	# Purpose: Displays the USB page
	#          
	# Inputs Code:  Application - self
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   None
	#
	# Outputs GUI:  Advances to movebar when USB drive is inserted
	# 				 into computer (through checkUSBs)
	#
	#################################################################
    def USB(self):
	global canUSBfile
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
	canUSBfile = 1
	
	################### moveBar #####################################
	# Purpose: Displays loading progress bar
	#          
	# Inputs Code:  None
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   None
	#
	# Outputs GUI:  Trackbar moves to end and Application advances to
	#			 	 Success page
	#################################################################
    def moveBar(self):
	global moveBarcount
	if (moveBarcount < 100):
	    self.UpLoader.step()
	    moveBarcount = moveBarcount + 1
	    self.after(30, self.moveBar)
	else:
	    moveBarcount = 0
	    self.Success()

	################### Success #####################################
	# Purpose: Displays Success page
	#          
	# Inputs Code:  Application - self
	# 	   
	# Outputs Code: None
	#          
	# Inputs GUI:   None
	#
	# Outputs GUI:  Advances to Start when USB drive is removed 
    #				 (through checkUSBs)
	#
	#################################################################
    def Success(self):
	global canUSBfile
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
	canUSBfile = 1
	
	
################### Main Program ################################
app = Application()
app.master.title('RG\'s Race')
w_0, h_0 = app.master.winfo_screenwidth(), app.master.winfo_screenheight()
app.master.geometry('%dx%d+0+0' % (w_0, h_0))
#app.master.wm_attributes('-type', 'splash')
app.master.protocol("WM_DELETE_WINDOW", dontDeleteWindow)
app.master.wm_attributes('-topmost', 'True')
app.mainloop()


################### End of Program ##############################
print ('\n-----End of Program-----\n')
