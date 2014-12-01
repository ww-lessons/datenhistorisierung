# coding=utf-8

from UserRepository import UserRepository
from datetime import datetime

import unittest

USERNAME = 'Mustermann.Max'


class NoHistoryMySQLTestCase(unittest.TestCase):
    def test_create_user(self):
        repo = UserRepository()
        user = repo.create_user(USERNAME)
        self.assertEqual(user.username, USERNAME)

    def test_list_users(self):
        repo = UserRepository()
        list = repo.list_users()

        for item in list:
            print item

        self.assertEqual(2, len(list))


    def test_update_user_empty(self):
        repo = UserRepository()
        user = repo.get_user_by_name(USERNAME)

        user.birth_date = None
        user.description = None
        user.assigned_rolename = None

        repo.update_user(user)

        user2 = repo.get_user_by_name(USERNAME)
        self.assertEqual(None, user2.birth_date)
        self.assertEqual(user.assigned_rolename, user2.assigned_rolename)
        self.assertEqual(user.description, user2.description)


    def test_update_user(self):
        repo = UserRepository()
        user = repo.get_user_by_name(USERNAME)

        user.birth_date = datetime.now()
        user.description = "Description"
        user.assigned_rolename = "Beispielrolle"

        repo.update_user(user)

        user2 = repo.get_user_by_name(USERNAME)
        self.assertNotEqual(None, user2.birth_date)
        self.assertEqual(user.assigned_rolename, user2.assigned_rolename)
        self.assertEqual(user.description, user2.description)


    def test_xdelete_user(self):
        repo = UserRepository()
        repo.delete_user(USERNAME)


if __name__ == '__main__':
    unittest.main()