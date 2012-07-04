#!/usr/bin/python
from pyaquos import controller
import web
class index:
	def GET(self):
		i = web.input(command=None, argument=None)
		print i.command
		print i.argument
		return render.index(i.command, i.argument)

if __name__ == "__main__":
	#aquos = controller('/dev/ttyUSB0')
	urls = ('/', 'index')
	app = web.application(urls, globals())
	render = web.template.render('html/')
	app.run()
