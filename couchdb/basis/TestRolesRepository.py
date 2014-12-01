from RolesRepository import RolesRepository

__author__ = 'wiw39784'

import unittest


DATABASE = 'demodb'


class MainTestCase(unittest.TestCase):
    def test_create_role(self):
        repo = RolesRepository(DATABASE)
        role = repo.create_role("MusterRole")
        self.assertEqual(role.rolename, "MusterRole")

    def test_list_roles(self):
        repo = RolesRepository(DATABASE)
        list = repo.list_roles()

        for item in list:
            print item

        self.assertEqual(1, len(list))


    def test_update_role_empty(self):
        repo = RolesRepository(DATABASE)
        role = repo.get_role_by_name("MusterRole")

        role.permissions = []

        repo.update_role(role)

        role2 = repo.get_role_by_name("MusterRole")
        self.assertEqual(role.id, role2.id)
        self.assertEqual(len(role.permissions), len(role2.permissions))


    def test_update_role(self):
        repo = RolesRepository(DATABASE)
        role = repo.get_role_by_name("MusterRole")

        role.permissions.append("Beispielrecht 1")
        role.permissions.append("Beispielrecht 2")
        role.permissions.append("Beispielrecht 3")

        repo.update_role(role)

        role2 = repo.get_role_by_name("MusterRole")
        self.assertEqual(role.id, role2.id)
        self.assertEqual(len(role.permissions), len(role2.permissions))


    def test_xdelete_role(self):
        repo = RolesRepository(DATABASE)
        repo.delete_role("MusterRole")


if __name__ == '__main__':
    unittest.main()

