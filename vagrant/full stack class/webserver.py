from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' \
				action='/hello'><h2>What would you like me to say?</h2>\
				<input name='message' type='text' ><input type='submit' \
				value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "&#161Hola!<a href = '/hello' >\
				Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' \
				action='/hello'><h2>What would you like me to say?</h2>\
				<input name='message' type='text' ><input type='submit' \
				value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h4><a href = '/restaurants/new'> \
				Make a new restaurant here</a></h4>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					output += "<p>%s</p>" % restaurant.name
					output += "<form action='/restaurant/%s/edit' \
					style='display:inline;'>" % restaurant.id
					output += "<input value='Edit' type='submit'></input>"
					output += "</form>"
					output += "<form action='http://google.com' style='display:inline;'>"
					output += "<input value='Delete' type='submit'></input>"
					output += "</form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ''
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' \
				action='/restaurants/new'><h3>Enter the name of the restaurant.</h3>\
				<input name='message' type='text' ><input type='submit' \
				value='Create'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				rest_id = self.path.split("/")[2]
				rest_to_update = session.query(Restaurant).filter_by(id = rest_id).one()

				if rest_to_update:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = "<html><body>"
					output += "<h1>%s</h1>" % rest_to_update.name
					output += "<form method='POST' enctype='multipart/form-data' \
					action='/restaurants/%s/edit'>" % rest_to_update.id
					output += "<input name='newRestName' type='text'\
					placeholder = '%s' >" % rest_to_update.name
					output += "<input type='submit' value='Rename'></form>" 
					output += "</body></html>"
					self.wfile.write(output)
					print output
					return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader(
				'content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				new_restaurant = Restaurant(name = messagecontent[0])
				session.add(new_restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader(
				'content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestName')

				rest_id = self.path.split("/")[2]

				rest_to_update = session.query(Restaurant).filter_by(id = rest_id).one()
				if rest_to_update:
					rest_to_update.name = messagecontent[0]
					session.add(rest_to_update)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
					return

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(("", port), WebServerHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()




if __name__ == "__main__":
	main()