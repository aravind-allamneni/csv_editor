#############################
# CSV FILE EDITOR APPLICATION
#############################

# Problem Statement
# Design a Web App that has the functionality to upload a CSV. Let’s say the CSV has fields Name, Age, Sex(M/F). The data inputted from CSV should be viewable in another page in a Tabular format with the option of editing existing entries. For each row in the tabular view, the user should be able to Edit/Delete Name, Age, Sex for each corresponding row entry.

# Database
# Option 1: Use an in-memory storage

# Option 2: Even better if there is a minimal backend server to make API calls to a Database, could be a local instance, to store data uploaded via CSV and to make edit/delete queries from the Tabular View Page.

# packages
from flask import Flask, request, redirect
from flask import render_template_string, render_template
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

# import psycopg2
# flak app instance
app = Flask(__name__)


# change the below line with your POSTGRES DB URL
SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    + os.getenv("DB_USER")
    + ":"
    + os.getenv("DB_PASSWORD")
    + "@localhost/csvstore"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
table_name = ""

# update row
@app.route("/update/<table_name>/<id>", methods=["POST"])
def update(table_name, id):
    data = request.form
    columns = []
    values = []
    if not data["index"]:
        return redirect("/update/" + str(table_name) + "/" + str(id))
    for key in data.keys():
        columns.append(key)
        values.append(data[key])
    colValStr = "SET " + str(columns[0]) + " = '" + str(values[0] + "'")
    for i in range(1, len(columns)):
        colValStr += str(", " + str(columns[i]) + " = '" + str(values[i]) + "'")

    stmt = (
        "UPDATE "
        + str(table_name)
        + "\n"
        + str(colValStr)
        + "\nWHERE index = "
        + str(id)
    )
    print(stmt)
    result = engine.execute(stmt)
    return redirect(str("/view/" + table_name))
    # return render_template_string(stmt)


# edit a row
@app.route("/edit/<table_name>/<id>", methods=["POST"])
def edit_row(table_name, id):
    stmt1 = (
        "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"
        + str(table_name)
        + "'"
    )
    result = engine.execute(stmt1)
    data = result.fetchall()
    print("data" + str(data))
    columns = []
    for item in data:
        # print(item)
        # print(type(item))
        columns.append(item[0])

    # return render_template_string(str(columns))
    return render_template(
        "editrecord.html", data=columns, table_name=table_name, id=id
    )

    # stmt = (
    #     "SELECT * FROM "
    #     + str(table_name)
    #     + " WHERE "
    #     + str(table_name)
    #     + ".index="
    #     + str(id)
    # )

    # print(str(data))
    # # return render_template("home.html", data=data, table_name=table_name)
    # return render_template_string(str(data))
    # return render_template("editrecord.html", data=data)


# delete a row
@app.route("/delete/<table_name>/<id>", methods=["POST"])
def delete_row(table_name, id):
    # DELETE FROM biostats WHERE biostats.index = 2
    stmt = (
        "DELETE FROM "
        + str(table_name)
        + " WHERE "
        + str(table_name)
        + ".index  = "
        + str(id)
    )
    # print(stmt)
    result = engine.execute(stmt)
    return redirect(str("/view/" + table_name))


# add arow
@app.route("/add/<table_name>", methods=["POST"])
def add_row(table_name):
    data = request.form
    # print(data)
    columns = []
    values = []
    for key in data.keys():
        columns.append(key)
        values.append(data[key])
    columnsStr = "(" + str(columns[0])
    for i in range(1, len(columns)):
        columnsStr += str(", " + str(columns[i]))
    columnsStr += str(")")

    valuesStr = "(" + str(values[0])
    for i in range(1, len(values)):
        valuesStr += str(", " + "'" + str(values[i]) + "'")
    valuesStr += str(")")

    stmt = "INSERT INTO " + str(table_name) + " " + columnsStr + "\nVALUES " + valuesStr
    # print(stmt)
    # return render_template_string(stmt)
    result = engine.execute(stmt)
    return redirect(str("/view/" + table_name))


# table view
@app.route("/view/<table_name>", methods=["POST", "GET"])
def home(table_name):
    # read the table fron db
    table_name = text(table_name)
    stmt = "SELECT * FROM " + str(table_name)
    result = engine.execute(stmt)
    data = result.fetchall()
    # print(data)
    return render_template("home.html", data=data, table_name=table_name)


# read data from csv
@app.route("/", methods=["POST", "GET", "DELETE"])
def read_csv():
    # render HTML Page
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        # get the file form form data
        csv_file = request.files["mycsvfile"]
        if not csv_file:
            return render_template("home.html")
        file_name = secure_filename(csv_file.filename)
        file_name = file_name[:-4]

        # read the csv to a pandas dataframe
        df = pd.read_csv(csv_file)

        # push teh dataframe to postgres db
        result = df.to_sql(file_name, engine, index=True, if_exists="replace")
        redirect_url = "/view/" + str(table_name)
        return redirect(str("/view/" + file_name))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
