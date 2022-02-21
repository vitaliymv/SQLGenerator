import os.path
import time

import pandas
from faker import Faker
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

list_choose = ['Name', 'Numbers', 'Job', 'ColorHex']

faker = Faker()


class Element:
    def __init__(self, id_element, name, type_element):
        self.id = id_element
        self.name = name
        self.type = type_element


@app.route("/")
def main():
    return render_template("index.html", list_choose=list_choose)


@app.route("/get-list")
def get_list():
    return jsonify(list_choose)


list_object = []


@app.route("/generate-sql", methods=["POST"])
def gen_sql():
    global json_data
    if request.method == "POST":
        json_data = request.get_json(True)
    return parse_json(json_data)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(path=filename, directory="")


def parse_json(data):
    global additional_data, count_data, format_data, table_name, input_data
    for obj in data:
        input_data = (obj.get("input_data"))
        additional_data = (obj.get("add_data"))

    for additional in additional_data:
        count_data = int(additional.get("count"))
        format_data = additional.get("format")
        table_name = additional.get("table_name")
    list_data = dict()
    for inp in input_data:
        list_data[inp.get("name")] = inp.get("type")
    string = f"""CREATE TABLE IF NOT EXISTS {table_name} (
    id int NOT NULL,\n\t{generate_string_for_table(list_data)}
);"""
    string_for_insert = f"""INSERT INTO {table_name}
VALUES 
    {generate_string_for_insert(count_data, list_data)}"""

    create_execute(string)
    create_execute(string_for_insert)
    time.sleep(5)
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    df = pandas.read_sql_query(f"SELECT * FROM {table_name}", sqlite_connection)
    a = pd.DataFrame(df)
    print(a)
    a.to_csv("file.csv")
    return string + "\n\n" + string_for_insert


def create_execute(query):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Connect successful")
        cursor.execute(query)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def generate_string_for_table(list_data):
    columns = ""
    for name in list_data.keys():
        columns += f"{name} {choose_type(list_data.get(name))},\n\t"
    return columns[0:len(columns) - 3]


def choose_type(title):
    if title == "Name":
        return "varchar(60)"
    if title == "Numbers":
        return "int"
    if title == "Job":
        return "varchar(50)"
    if title == "ColorHex":
        return "varchar(10)"


def generate_string_for_insert(counter, list_data):
    query = ""
    for i in range(1, counter + 1):
        query += f"({i}, "
        for name in list_data.keys():
            query += f"'{choose_fake(list_data.get(name))}', "
        query = query[0:len(query) - 2]
        query += "),\n\t"
    return query[0:len(query) - 3]


def choose_fake(title):
    if title == "Name":
        return faker.name()
    if title == "Numbers":
        return faker.pyint(min_value=0, max_value=100)
    if title == "Job":
        job = faker.job()
        job_split = job.split(",")
        job_new = "".join(job_split)
        return job_new
    if title == "ColorHex":
        return faker.hex_color()


if __name__ == "__main__":
    app.run(debug=True)
