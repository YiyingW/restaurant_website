from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

## Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine 
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here </a>"
                output += "</br></br>"
                for restaurant in restaurants:
                    output += restaurant.name 
                    output += "</br>"
                    output += "<a href='/%s/edit'>Edit </a>" % str(restaurant.id)
                    output += "</br>"
                    output += "<a href='/%s/delete'>Delete </a>" % str(restaurant.id)
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant </h1>"
                output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit") or self.path.endswith('/delete'):
                restaurant_id = int(self.path.split('/')[-2])
                this_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if self.path.endswith("/edit"):
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s </h1>" % this_restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action ='/%s/edit'>" % str(this_restaurant.id)
                    output += "<input name='newName' type='text' placeholder='%s'>" % this_restaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                if self.path.endswith("/delete"):
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s ?</h1>" % this_restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action ='/%s/delete'>" % str(this_restaurant.id)
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return

            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except:
            pass

    def do_POST(self):

        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant class
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newName')

                # Create new Restaurant class
                restaurant_id = int(self.path.split('/')[-2])
                this_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                this_restaurant.name = messagecontent[0]
                session.add(this_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            if self.path.endswith("/delete"):
                restaurant_id = int(self.path.split('/')[-2])
                this_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                session.delete(this_restaurant)
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
        port = 9110
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()