# coding=utf-8

from model import User, ModelUtility


class UserRepository():
    # Verbindung zur Datenbank initialisieren
    def __init__(self):
        self.db = ModelUtility.db
        ModelUtility.Base.metadata.create_all(self.db)
        self.session = ModelUtility.SessionFactory()


    # Benutzer anlegen
    def create_user(self, username, rolename=None):
        u = User(username=username)
        u.assigned_role_name = rolename
        self.session.add(u)
        self.session.commit()
        return u


    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_user_by_name(self, username):
        u = self.session.query(User).filter(User.username == username).first()
        return u


    # Benutzer aktualisieren
    def update_user(self, user):
        u = self.session.query(User).filter(User.username == user.username).first()

        u.assigned_role_name = user.assigned_rolename
        u.birth_date = user.birth_date
        u.description = user.description

        self.session.add(u)
        self.session.commit()


    # Benutzer loeschen
    def delete_user(self, username):
        u = self.session.query(User).filter(User.username == username).first()
        self.session.delete(u)
        self.session.commit()


    # Eine Liste der Benutzer-Objekte erstellen
    def list_users(self):
        return self.session.query(User).order_by(User.username).all()
