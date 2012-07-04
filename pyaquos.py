import serial

class pyaquos:
	"""
	This is a class for controlling SHARP Aquos LC-32D59U, LC-42D59U, and 
	possibly other model LCD televisions via their RS-232 serial interface.
	"""
	def __init__(ttyname):
	"""
	Generate a new pyaquos interface object
	@type ttyname:		string
	@param ttyname:		the dev file for the serial interface (often 
						/dev/ttyUSB0 for USB serial adapters)
	"""
		self.tty = serial.Serial(ttyname, 9600)
		self.ok = True

	def power(state):
	"""
	Power cycle the TV.
	@type state:		bool
	@param state:		The power state for the TV.  True is ON, False is OFF.
	@return:			A boolean set to True if the command ran succesfully.
	"""
		if state:
			return self.sendcommand('POWR1   \r\n')
		else:
			return self.sendcommand('POWR0   \r\n')

	def volume(level):
	"""
	Change the volume on the TV.
	@type level:		int
	@param level:		The volume level for the TV, from 1 to 99 (low to high)
	@return:			A boolean set to True if the command ran succesfully.
	"""
		if level < 100 and level > 0:#The volume can range from 1 to 99
			return self.command('VOLM%02d  \r\n' % (level))
		else:
			raise ValueError

	def mute(state):
	"""
	Mute the TV.
	@type state:		bool
	@param state:		The muting state.  True is muted, False is unmuted.
	@return:			A boolean set to True if the command ran succesfully.
	"""
		if state:
			return self.command('MUTE1   \r\n')
		else:
			return self.command('MUTE2   \r\n')

	def input(number):
	"""
	Change the A/V Source for the TV
	@type number:		int
	@param number:		The input number for the TV.
	@return:			A boolean set to True if the command ran succesfully.
	"""
		if number < 9 and number > 0:#There are 8 inputs
			#For the LC-32D59U, the inputs are:
			#INPUT1: HDMI1 Top Side HDMI
			#INPUT2: HDMI2 Bottom Side HDMI
			#INPUT3: HDMI3 Top Rear HDMI
			#INPUT4: HDMI4 Bottom Rear HDMI
			#INPUT5: COMP1 Top Rear Component
			#INPUT6: COMP2 Bottom Rear Component
			#INPUT7: AV Rear Composite
			#INPUT8: PC IN VGA PC input
			return self.command('IAVD%1d   \r\n' % (number))
		else:
			raise ValueError

	def sendcommand(commandstring):
	"""
	Internal method for sending the commands and checking the return code.
	@type commandstring:	string	
	@param commandstring:	The command to be passed to the TV over RS-232.
	@return:				A boolean set to True if the command ran succesfully
	"""
		self.tty.write(commandstring)
		response = self.tty.readline()
		if response == 'OK\r\n':
			return True
		else:
			return False
