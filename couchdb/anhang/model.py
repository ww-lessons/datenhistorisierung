# coding=utf-8

#
# Datenmodell zur Historisierung mit Python und Couchdb
#
import couchdb
import couchdb.mapping

from couchdb.mapping import TextField, DateField, DateTimeField, ListField, DictField, Mapping


# Benutzer, der genau eine Rolle zugeordnet bekommen haben kann
class User(couchdb.mapping.Document):
    username = TextField()
    description = TextField()
    birth_date = DateField()
    assigned_rolename = TextField()
    create_date = DateTimeField()
    change_date = DateTimeField()
    type = TextField()


# Rolle, die verschiedene Berechtigungen besitzen kann
class Role(couchdb.mapping.Document):
    rolename = TextField()
    permissions = ListField(TextField())
    create_date = DateTimeField()
    created_by = TextField()
    change_date = DateTimeField()
    type = TextField()