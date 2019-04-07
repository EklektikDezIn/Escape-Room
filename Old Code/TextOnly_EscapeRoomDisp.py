
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
import pyudev, time, os

# define global constants and Booleans
cont = False
context = pyudev.Context()
debug = False
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
passfile = open('passwords.txt', 'r')
password = passfile.readline().strip()

# define functions
def pollfordrive():
    for device in iter(monitor.poll, None):
        if device.action =='add':
	    if (debug):
	        print('You have plugged a device into the computer')
                print('{} connected'.format(device))
	    return 1
        if device.action =='remove':
            if (debug):
	        print('You have unplugged a device from the computer')
                print('{} disconnected'.format(device))
	    return 0

def calctdiff(Stt, Fnt):
    Total=Fnt-Stt
    if (debug):
	print('The total time is %f' % Total)
    Minutes = int(Total/60)
    if (debug):
	print('The total number of minutes is %d' % Minutes)
    Seconds = int(Total % 60 )
    if (debug):
	print('The total number of seconds  is %d' % Seconds)
    return ('%02d:%02d' % (Minutes, Seconds))

def donoth():
    print ('')
# ===== Main Program =====
while(True):
    cont = False
    ignvar = os.system ('clear')
    if (debug):
        print ('DEBUG: The password is: %s' % password)

    raw_input('Press enter to continue...')
    startTime=time.time()
    if (debug):
        print ('DEBUG: The starting time is: %f' % startTime)

    while (cont == False):
        enteredpass = raw_input('Please enter the password: ')
        if (debug):
            print ('DEBUG: The entered password is: %s' % enteredpass)
        if (enteredpass == password):
            print ('That is the correct password!')
            cont = True
        else:
            print ('That is not the correct password')

    print ('Please insert the flashdrive with the file')
    while (pollfordrive() != 1):
        donoth()
    print ('You did it!')
    print ('It took you %s to complete this!' % calctdiff(startTime, time.time()))
    while (pollfordrive() != 0):
        donoth()
    print ('Resetting System...')
    time.sleep(1)

# End of Program
print ('\n-----End of Program-----\n')
