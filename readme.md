#############################
# CSV FILE EDITOR APPLICATION
#############################

A Web App that has the functionality to upload a CSV. Let’s say the CSV has fields Name, Age, Sex(M/F). The data inputted from CSV should be viewable in another page in a Tabular format with the option of editing existing entries. For each row in the tabular view, the user should be able to Edit/Delete Name, Age, Sex for each corresponding row entry.

# Database
An in-memory storage

# required packages
flask
sqlalchemy
pandas
werkzeug.utils
os
python-dotenv

# .env file
add the following values to .env file
DB_USER : postgres db user
DB_PASSWORD : postgres db password

# create a database names "csvstore" on your postgres instance
database name : csvstore incase you want to use an existing db change the postgres url on line 29 of app.py
change line 29 on app.py to reflect the URL of your postgres instance
URL format need to be : postgresql://<username>:<password>@localhost/csvstore"

# how to run
open the terminal in your project folder and run 
> python app.py
This will host a server on port: 5001
navigate to localhost:5001 on your browser and use the app

# Limitations
1. No security features like data validation, cleaning special characters from inputs etc is added
2. No middleware for preprocessing of inputs
3. No login or authentication for users
4. Will work only for limited sizes of csv files for larger files streaming need to be used to allow for GBs of data to be uploaded and edited

