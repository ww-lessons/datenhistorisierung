# coding=utf-8

from RoleRepository import RoleRepository

repo = RoleRepository()

# Die Musterrolle wird für die Unit-Test in TestUserRepository benötigt
repo.create_role("Beispielrolle", [])
