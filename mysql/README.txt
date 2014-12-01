Vorbereitung der Datenbank
==========================

create database historisierung_none;
grant all privileges on historisierung_none.* to 'demo'@'localhost' identified by 'demo';

create database historisierung_simple;
grant all privileges on historisierung_simple.* to 'demo'@'localhost';

create database historisierung_full;
grant all privileges on historisierung_full.* to 'demo'@'localhost';


Connection-Strings in SQL-Alchemy
=================================

mysql+mysqlconnector://demo:demo@localhost:3306/historisierung_none
mysql+mysqlconnector://demo:demo@localhost:3306/historisierung_simple
mysql+mysqlconnector://demo:demo@localhost:3306/historisierung_full