# Controller-Klasse

__author__ = 'wiw39784'

import couchdb
from model import User
from datetime import datetime


class UserRepository():

    TYPE_KEY = 'user_inobject_hist'

    # Verbindung zur Datenbank initialisieren
    def __init__(self, db_name):
        server = couchdb.client.Server()

        if server.__contains__(db_name):
            self.db = server[db_name]
        else:
            self.db = server.create(db_name)


    # Benutzer anlegen
    def create_user(self, username, rolename=None):
        u = User(username=username, assigned_rolename=rolename)
        u.id = self.calculate_id(username)
        u.type = self.TYPE_KEY
        u.store(self.db)
        return u


    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_user_by_name(self, username):
        u = User.load(self.db, self.calculate_id(username))
        return u


    # Benutzer aktualisieren
    def update_user(self, user):
        u = User.load(self.db, user.id)

        # 1. Alte Werte in die Historie schreiben
        u.previous_versions.append(
            description=u.description,
            assigned_rolename=u.assigned_rolename,
            version_create_date=u.change_date,
            version_created_by='UNBEKANNT',
            version_valid_until=datetime.now()
        )

        # 2. Aktuellen Zustand aktualisieren
        u.assigned_rolename = user.assigned_rolename
        u.birth_date = user.birth_date
        u.description = user.description

        u.store(self.db)


    # Benutzer loeschen
    def delete_user(self, username):
        del self.db[self.calculate_id(username)]


    # Eine Liste der Benutzer-Objekte erstellen
    def list_users(self):
        map_function = "function(doc) { if(doc.type =='"+self.TYPE_KEY+"') { emit(doc.username, doc); }}"
        return self.db.query(map_function)


    # Private Methode: IDs fuer Benutzer aus deren Benutzernamen berechnen
    def calculate_id(self, username):
        return '{0}|{1}'.format(self.TYPE_KEY, username)