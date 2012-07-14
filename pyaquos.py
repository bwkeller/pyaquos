import serial

class controller:
	"""
	This is a class for controlling SHARP Aquos LC-32D59U, LC-42D59U, and 
	possibly other model LCD televisions via their RS-232 serial interface.
	"""
	def __init__(self, ttyname):
		"""
		Generate a new pyaquos interface object
		@type ttyname:	string
		@param ttyname:	the dev file for the serial interface (often 
						/dev/ttyUSB0 for USB serial adapters)
		"""
		self.tty = serial.Serial(ttyname, 9600)
		self.ok = True

	def lock_power(self, state):
		"""
		Enable/disable the use of the power() command.
		@type state:	bool
		@param state:	True if the power() command is to be disabled.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if state:
			return self.send_command('RSPW0   \r\n')
		else:
			return self.send_command('POWR1   \r\n')

	def lock_state(self):
		"""
		Power cycle the TV.
		@return:		Boolean set to True if the power() command is disabled.
		"""
		if self.query_state('RSPW?   \r\n') == '1':
			return True
		else:
			return False

	def power(self, state):
		"""
		Power cycle the TV.
		@type state:	bool
		@param state:	The power state for the TV.  True is ON, False is OFF.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if state:
			return self.send_command('POWR1   \r\n')
		else:
			return self.send_command('POWR0   \r\n')

	def power_state(self):
		"""
		Power cycle the TV.
		@return:		A boolean set to True if the TV is currently powered on.
		"""
		if self.query_state('POWR?   \r\n') == '1':
			return True
		else:
			return False

	def volume(self, level):
		"""
		Change the volume on the TV.
		@type level:	int
		@param level:	The volume level for the TV, from 1 to 99 (low to high)
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if level < 100 and level > 0:#The volume can range from 1 to 99
			return self.send_command('VOLM%02d  \r\n' % level)
		else:
			raise ValueError('Volume must be between 1 and 99')

	def volume_state(self):
		"""
		Query the current volume level of the TV.
		@return:		An integer storing the current volume level of the TV.
		"""
        return int(self.query_state('VOLM??  \r\n'))

	def screen_position(self, horizontal, vertical, clock, phase):
		"""
		Change the VGA screen position, clock, and phase (this may be dangerous)
		I honestly don't know what clock and phase really do.
		@type horizontal:	int
		@param horizontal:	Horizontal offset (0-100)
		@type vertical:		int
		@param vertical:	Vertical offset (0-100)
		@type clock:		int
		@param clock:		Clock frequency (0-180)
		@type phase:		int
		@param phase:		Phase offset (0-40)
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if horizontal < 0 or horizontal > 100:
			raise ValueError('Horizontal offset must be between 0 and 100')
		if vertical < 0 or vertical > 100:
			raise ValueError('Vertical offset must be between 0 and 100')
		if clock < 0 or clock > 180:
			raise ValueError('Clock Frequency must be between 0 and 180')
		if phase < 0 or phase > 40:
			raise ValueError('Phase offset must be between 0 and 40')
		hreturn = self.send_command('HPOS%03d \r\n' % horizontal)
		vreturn = self.send_command('VPOS%03d \r\n' % vertical)
		clckreturn = self.send_command('CLCK%03d \r\n' % clock)
		phsreturn = self.send_command('PHSE%03d \r\n' % phase)
		return hreturn and vreturn and clckreturn and phase

    def screen_state(self):
        """
        Return the current VGA screen settings.
        @return:    (int, int, int, int) of the horizontal offset, vertical 
        offset, clock frequency and phase.
        """
        horizontal = int(self.query_state('HPOS??? \r\n'))
        vertical = int(self.query_state('VPOS??? \r\n'))
        clock = int(self.query_state('CLCK??? \r\n'))
        phase = int(self.query_state('PHSE??? \r\n'))
        return (horizontal, vertical, clock, phase)

	def mute(self, state):
		"""
		Mute the TV.
		@type state:	bool
		@param state:	The muting state.  True is muted, False is unmuted.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if state:
			return self.send_command('MUTE1   \r\n')
		else:
			return self.send_command('MUTE2   \r\n')

	def mute_state(self):
		"""
        Query if the TV is muted
		@return:		A boolean set to True if TV is muted.
		"""
        if self.query_state('MUTE?   \r\n') == '1':
            return True
        else:
            return False

	def input_toggle(self):
		"""
		Toggle your way through the inputs.  This moves down through the 
		inputs, and loops back to INPUT1 after being called on INPUT8.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		return self.send_command('ITGD1   \r\n')

	def input_tv(self):
		"""
		Switch to the TV tuner.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		return self.send_command('ITVD0   \r\n')

	def input_num(self, number):
		"""
		Change the A/V Source for the TV
		@type number:	int
		@param number:	The input number for the TV.
		@return:		A boolean set to True if the command ran succesfully.
		"""
		if number < 9 and number > 0:#There are 8 inputs
			#For the LC-32D59U, the inputs are:
			#INPUT0: TV Tuner (use input_tv() to access this)
			#INPUT1: HDMI1 Top Side HDMI
			#INPUT2: HDMI2 Bottom Side HDMI
			#INPUT3: HDMI3 Top Rear HDMI
			#INPUT4: HDMI4 Bottom Rear HDMI
			#INPUT5: COMP1 Top Rear Component
			#INPUT6: COMP2 Bottom Rear Component
			#INPUT7: AV Rear Composite
			#INPUT8: PC IN VGA PC input
			return self.send_command('IAVD%1d   \r\n' % (number))
		else:
			raise ValueError('Input must be between 1 and 8')

    def input_state(self):
        """
        Return the current input number of the TV.
        @return:        The integer number corresponding to the current input.
        """
        return int(self.query_state('IAVD?   \r\n'))

	def query_state(self, commandstring):
		"""
		Internal method for checking the state of some TV parameter.
		@type commandstring:	string	
		@param commandstring:	The command to be passed to the TV over RS-232.
		@return:				The returned value.
		"""
		self.tty.write(commandstring)
		response = self.tty.readline()
		return response[:-2]

	def send_command(self, commandstring):
		"""
		Internal method for sending the commands and checking the return code.
		@type commandstring:	string	
		@param commandstring:	The command to be passed to the TV over RS-232.
		@return:			A boolean set to True if the command ran succesfully
		"""
		self.tty.write(commandstring)
		response = self.tty.readline()
		if response == 'OK\r\n':
			return True
		else:
			return False
