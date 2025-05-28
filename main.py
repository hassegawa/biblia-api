from fastapi import FastAPI, Query
import sqlite3
from typing import Optional, List, Dict
import json
import random
import datetime

app = FastAPI()

def get_data_from_db(book, chapter, verse, endverse: Optional[str]) -> List[Dict]:
    conn = sqlite3.connect('nvi.db')
    cursor = conn.cursor()

    sql = "SELECT t.name, b.name, b.abbrev, v.chapter, v.verse, v.text " \
            "FROM testament AS t " \
      "INNER JOIN books     AS b ON t.id = b.testament " \
      "INNER JOIN verses    AS v ON b.id = v.book " \
           "WHERE 1=1 " 
    
    params = []

    print("book", book)

    if book:
        sql += " AND b.name = ?"
        params.append(book)
    if chapter:
        sql += " AND v.chapter = ?"
        params.append(chapter)
    if endverse:
        sql += " AND v.verse BETWEEN ? AND ?"
        params.extend([verse, endverse])
    else:
        if verse:
            sql += " AND v.verse = ?"
            params.append(verse)  

    sql += " LIMIT 10 "

    #sql = "SELECT * FROM verses b WHERE 1=1 LIMIT 100"
    #print(sql)            

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(col_names, row)) for row in rows]

@app.get("/verse")
def select_verse(
    book: Optional[str] = Query(None),
    chapter: Optional[str] = Query(None),
    verse: Optional[int] = Query(None),
    endverse: Optional[int] = Query(None)
):
    return {"verse": get_data_from_db(book, chapter, verse, endverse)}

def get_books_from_db() -> List[Dict]:
    conn = sqlite3.connect('nvi.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM books b WHERE 1=1"

    cursor.execute(sql)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(col_names, row)) for row in rows]


@app.get("/")
def index():
    return {"books": get_books_from_db()}

# Read JSON file
def read_json(path_file_daily_list):
    with open(path_file_daily_list, 'r') as file:
        data = json.load(file)
    return data

# Function to randomize an item from the "verses" list
def randomize_item(data):
    # Assuming the JSON file has the key "verses" containing a list of items
    randomized_item = random.choice(data)
    return randomized_item

# Caminho do arquivo JSON
path_file_daily_list = 'daily.json'

@app.get("/daily")
def daily():
    return get_daily()

def get_daily():    
    data = read_json(path_file_daily_list)

    datetime_now = datetime.datetime.now()

    for item in data:
        if item["month"] == datetime_now.month and item["day"] == datetime_now.day:
            # If the item's month and day match the current month and day, return the item
            return {"verse": get_data_from_db(item["book"], item["chapter"], item["verse"], item["verse_end"])}

    item = randomize_item(data)
    
    return {"verse": get_data_from_db(item["book"], item["chapter"], item["verse"], item["verse_end"])}


@app.get("/today")
def today():
    dados = get_daily()

    d = dados["verse"]
    message = []

    for i in d:
        message.append(f"{i['verse']} - {i['text']}")

    return { "message" : f" {d[0]['name']} {d[0]['chapter']} , {' '.join(message)}" } 

@app.get("/random")
def today():
    dados = read_json(path_file_daily_list)

    item = randomize_item(dados)
    
    return {"verse": get_data_from_db(item["book"], item["chapter"], item["verse"], item["verse_end"])}

@app.get("/check")
def check():
    data = read_json(path_file_daily_list)
    errors = []

    for item in data:
        db = get_data_from_db(item["book"], item["chapter"], item["verse"], item["verse_end"]) 
 
        try:
            print(len(db[0]))
    
        except IndexError:  
            # If there is no result, it means the query failed
            errors.append(item)
    
    return {"errors": errors }


