#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Todo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        seznam = Todo.query(Todo.stanje == False).fetch()
        seznam_done = Todo.query(Todo.stanje == True).fetch()

        params = {
            "seznam": seznam,
            "seznam_done": seznam_done
        }
        return self.render_template("index.html", params=params)

    def post(self):
        ime = self.request.get("ime")
        opis = self.request.get("opis")
        nov_todo = Todo(ime=ime, opis=opis)
        nov_todo.put()
        seznam = Todo.query().fetch()
        params = {
            "seznam": seznam
        }
        return self.render_template("success.html", params=params)


class EditHandler(BaseHandler):
    def get(self, todo_id):
        todo = Todo.get_by_id(int(todo_id))
        params = {"todo": todo}
        return self.render_template("edit.html", params=params)

    def post(self, todo_id):
        ime = self.request.get("ime")
        opis = self.request.get("opis")
        stanje = self.request.get("stanje")
        todo = Todo.get_by_id(int(todo_id))
        todo.ime = ime
        todo.opis = opis
        if stanje == "on":
            todo.stanje = True
        else:
            todo.stanje = False
        todo.put()
        return self.render_template("success.html")


class DeleteHandler(BaseHandler):
    def get(self, todo_id):
        todo = Todo.get_by_id(int(todo_id))
        params = {"todo": todo}
        return self.render_template("delete.html", params=params)

    def post(self, todo_id):
        todo = Todo.get_by_id(int(todo_id))
        todo.key.delete()
        return self.render_template("success.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="seznam-todo"),
    webapp2.Route('/edit/<todo_id:\d+>', EditHandler),
    webapp2.Route('/delete/<todo_id:\d+>', DeleteHandler),
], debug=True)
