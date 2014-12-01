# coding=utf-8

from UserRepository import UserRepository

__author__ = 'wiw39784'

import unittest

# from model import User
from datetime import datetime

DATABASE = 'demodb'
USERNAME = 'Musteruser.Max'


class MyTestCase(unittest.TestCase):
    def test_create_user(self):
        repo = UserRepository(DATABASE)
        user = repo.create_user(USERNAME)
        self.assertEqual(user.username, USERNAME)

    def test_list_users(self):
        repo = UserRepository(DATABASE)
        list = repo.list_users()

        for item in list:
            print item

        self.assertEqual(1, len(list))


    def test_update_user_empty(self):
        repo = UserRepository(DATABASE)
        user = repo.get_user_by_name(USERNAME)

        user.birthdate = None
        user.description = None
        user.assigned_rolename = None

        repo.update_user(user)

        user2 = repo.get_user_by_name(USERNAME)
        self.assertEqual(user.id, user2.id)
        self.assertEqual(None, user2.birthdate)
        self.assertEqual(user.assigned_rolename, user2.assigned_rolename)
        self.assertEqual(user.description, user2.description)


    def test_update_user(self):
        repo = UserRepository(DATABASE)
        user = repo.get_user_by_name(USERNAME)

        user.birthdate = datetime.now()
        user.description = "Description"
        user.assigned_rolename = "Beispielrolle"

        repo.update_user(user)

        user2 = repo.get_user_by_name(USERNAME)
        self.assertNotEqual(None, user2.birthdate)
        self.assertEqual(user.assigned_rolename, user2.assigned_rolename)
        self.assertEqual(user.description, user2.description)


    def test_xdelete_user(self):
        repo = UserRepository(DATABASE)
        repo.delete_user(USERNAME)


if __name__ == '__main__':
    unittest.main()
