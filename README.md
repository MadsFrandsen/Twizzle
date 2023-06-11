# Twizzle
Repo for Twizzle! A social media platform heavily inspired by twitter. 

This project was created as part of the database course Databases and Information Systems at The University of Copenhagen. Objective is to become familiar with PostgreSQL and web development using Python and the Flask API as our tools. 

Credit goes to Corey Schafer and his Flask turtorial - https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH


## Initialization ✔

Clone / download repository files and run the following to install the required packages preferably within a fresh virtual python environment:

    pip install -r requirements.txt

Create a new database in pgAdmin, postico or whatever tool you are using for postgreSQL. Preferably name the database Twizzle and add the following to your .env file (normally .env should be a private file containing user secrets, in this case we have kept it inside the project files for easy
access for the TAs):

    EMAIL_USER = <user_email_address>
    EMAIL_PASS = <user_email_address_pass>
    SECRET_KEY = <secret_key>
    DB_NAME = Twizzle || <postgres_db_name>
    DB_USERNAME = postgres || <postgres_user_name>
    DB_PASSWORD = <postgres_user_password>

The values are already set in the file with what we used when running the code, aside from the email info which we obviously have not included. You do not have to set the email related fields to anything, but without them you will not be able to reset your password. If you do decide to set them, then make sure that you are using a gmail address with 2FA and an app password. Info can be found here: https://www.youtube.com/watch?v=Jp9B0rY6Fxk

When the information is present and correct, the server can be started with:

    python run.py 

while standing in the root root directory of the project. In the __init__.py file in the /twizzle directory, you can also change the host and the port number of the server. By default the port is set to 5123 as this was the port we used.

## Folder setup 📁


