
import webapp2
import jinja2
import os
import spellcheck as sc
jinja_environment = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
class MainPage(webapp2.RequestHandler):
    def get(self):
        template 	= jinja_environment.get_template('main.html')
        self.response.out.write(template.render())
    def post(self):
        sentence = self.request.get("content")
        render   = {}
        render["s"] = sentence
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(render))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
