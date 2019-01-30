from google.appengine.ext import ndb

class Todo(ndb.Model):
    ime = ndb.StringProperty()
    opis = ndb.StringProperty()
    stanje = ndb.BooleanProperty(default=False)