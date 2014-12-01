# coding=utf-8

import couchdb
import json
from model import Role
from datetime import datetime


class RolesRepository():

    TYPE_KEY = 'role_attachment_hist'

    # Verbindung zur Datenbank initialisieren
    def __init__(self, db_name):
        server = couchdb.client.Server()

        if server.__contains__(db_name):
            self.db = server[db_name]
        else:
            self.db = server.create(db_name)

    # Benutzer anlegen
    def create_role(self, rolename, permissions=[]):
        r = Role(rolename=rolename, permissions=permissions)
        r.id = self.calculate_id(rolename)
        r.create_date = datetime.now()
        r.change_date = r.create_date
        r.created_by = "UNBEKANNT"
        r.type = self.TYPE_KEY
        r.store(self.db)
        return r

    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_role_by_name(self, rolename):
        r = Role.load(self.db, self.calculate_id(rolename))
        return r

    # Benutzer aktualisieren
    def update_role(self, role):
        # 1. Bisherigen Stand in die Historie schreiben
        # self.db.add_attachment
        r_doc = self.db[role.id]
        json_string = json.dumps(r_doc)
        filename = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.put_attachment(r_doc, json_string, filename, content_type='application/json')

        # 2. Daten aktualisieren
        r = Role.load(self.db, role.id)
        r.permissions = role.permissions
        r.change_date = datetime.now()
        r.store(self.db)

    # Benutzer loeschen
    def delete_role(self, rolename):
        del self.db[self.calculate_id(rolename)]

    # Eine Liste der Benutzer-Objekte erstellen
    def list_roles(self):
        map_function = "function(doc) { if(doc.type =='"+self.TYPE_KEY+"') { emit(doc.rolename, doc); }}"
        return self.db.query(map_function)

    # Änderungshistorie des Benutzers ermitteln
    def get_history(self, rolename):
        map_function = "function(doc) { if(doc.type =='"+self.TYPE_KEY+"' && doc.rolename=='"+rolename+"')" \
                       "{ for(var key in doc._attachments) { " \
                       "var obj = doc._attachments[key]; " \
                       "emit(doc.rolename, {'key':key, 'value':obj}); }}}"

        result = []
        u = self.db.query(map_function)
        for row in u:
            # print row.id, row.value['key']
            attachment_str = self.db.get_attachment(row.id, row.value['key'])
            attachment = json.load(attachment_str)
            result.append(attachment)

        return result

    # Private Methode: IDs fuer Benutzer aus deren Benutzernamen berechnen
    def calculate_id(self, rolename):
        return '{0}|{1}'.format(self.TYPE_KEY, rolename)