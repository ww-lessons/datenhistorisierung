# coding=utf-8

#
# Datenmodell zur Historisierung mit Python und Couchdb
#
import couchdb
import couchdb.mapping

from couchdb.mapping import TextField, DateField, DateTimeField, ListField


# Benutzer, der genau eine Rolle zugeordnet bekommen haben kann
class User(couchdb.mapping.Document):
    username = TextField()
    description = TextField()
    birthdate = DateField()
    assigned_rolename = TextField()
    type = TextField()


# Rolle, die verschiedene Berechtigungen besitzen kann
class Role(couchdb.mapping.Document):
    rolename = TextField()
    permissions = ListField(TextField())
    last_change_date = DateTimeField()
    last_changed_by = TextField()
    type = TextField()