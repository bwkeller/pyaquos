#!/usr/bin/python
from pyaquos import controller
import web
class index:
	def GET(self):
		return 'Hello World'

if __name__ == "__main__":
	#aquos = controller('/dev/ttyUSB0')
	urls = ('/', 'index')
	app = web.application(urls, globals())
	app.run()
