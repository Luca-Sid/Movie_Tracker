@echo off
SET DB_NAME=test
SET DB_USER=root
SET DB_PASS=CLAITA04
SET SQL_DB=db/create_db.sql
SET SQL_USER=db/add_admin.sql

echo Dropping database %DB_NAME%...
mysql -u %DB_USER% -p%DB_PASS% -e "DROP DATABASE IF EXISTS %DB_NAME%;"
echo Database %DB_NAME% dropped successfully.

echo Creating database %DB_NAME%...
mysql -u %DB_USER% -p%DB_PASS% -e "CREATE DATABASE %DB_NAME%;"
echo Database %DB_NAME% created successfully.

echo Building database from file %SQL_DB%...
mysql %DB_NAME% -u %DB_USER% -p%DB_PASS% < %SQL_DB%
echo Database %DB_NAME% built successfully.

echo Adding admin user...
mysql %DB_NAME% -u %DB_USER% -p%DB_PASS% < %SQL_USER%
echo Admin added successfully.

pause
