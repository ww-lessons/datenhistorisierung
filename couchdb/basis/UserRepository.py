# Controller-Klasse

__author__ = 'wiw39784'

import couchdb
from model import User


class UserRepository():
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
        u.type = 'user'
        u.store(self.db)
        return u


    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_user_by_name(self, username):
        u = User.load(self.db, self.calculate_id(username))
        return u


    # Benutzer aktualisieren
    def update_user(self, user):
        u = User.load(self.db, user.id)

        u.assigned_rolename = user.assigned_rolename
        u.birthdate = user.birthdate
        u.description = user.description

        u.store(self.db)


    # Benutzer loeschen
    def delete_user(self, username):
        del self.db[self.calculate_id(username)]


    # Eine Liste der Benutzer-Objekte erstellen
    def list_users(self):
        map_function = "function(doc) { if(doc.type =='user') { emit(doc.username, doc); }}";
        return self.db.query(map_function)


    # Private Methode: IDs fuer Benutzer aus deren Benutzernamen berechnen
    @staticmethod
    def calculate_id(username):
        return 'user|' + username