-- Prepares a MySQL server for the Home Physio project

CREATE DATABASE IF NOT EXISTS home_physio_db;
CREATE USER IF NOT EXISTS 'home_physio'@'localhost';
GRANT ALL PRIVILEGES ON home_physio_db.* TO 'home_physio'@'localhost';
FLUSH PRIVILEGES;
