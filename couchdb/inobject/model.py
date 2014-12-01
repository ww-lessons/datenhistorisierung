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
    previous_versions = ListField(DictField(Mapping.build(
        description=TextField(),
        assigned_rolename=TextField(),
        version_create_date=DateTimeField(),
        version_created_by=TextField(),
        version_valid_until=DateTimeField(),
    )))


# Rolle, die verschiedene Berechtigungen besitzen kann
class Role(couchdb.mapping.Document):
    rolename = TextField()
    permissions = ListField(TextField())
    create_date = DateTimeField()
    created_by = TextField()
    change_date = DateTimeField()
    type = TextField()
    previous_versions = ListField(DictField(Mapping.build(
        permissions=ListField(TextField()),
        version_create_date=DateTimeField(),
        version_created_by=TextField(),
        version_valid_until=DateTimeField()
    )))