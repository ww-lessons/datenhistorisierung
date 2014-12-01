# coding=utf-8


class User():
    def __init__(self, username, create_date=None,
                 deleted=False, description="",
                 birthdate=None, assigned_rolename=None):
        self.username = username
        self.create_date = create_date
        self.deleted = deleted
        self.description = description
        self.birthdate = birthdate
        self.assigned_rolename = assigned_rolename
