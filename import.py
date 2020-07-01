import psycopg2
import re
import csv

#import sys
#import io
#from io import StringIO
#line_buffering=True
conn = psycopg2.connect('host=ec2-34-225-82-212.compute-1.amazonaws.com dbname=d64djukmaep4ov user=xkirkgsdjndrtd password=04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b')
cur = conn.cursor()
with open('books1.csv', 'r+') as f: #to open and close the csv file automatically
    #reader = csv.reader(f)
    #next(f) #to skip the header row
    reader = csv.reader(f, delimiter = ',', lineterminator='\n' , dialect = csv.excel)
    for row in reader:
        if row[2] != '':
            cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)", row)
        #else:
        #    split_row = row[0].split('"')
        #    second_split = split_row[2].split(',')
        #    second_split.insert(0, split_row[0])
        #    second_split.insert(1, split_row[1])
        #    remove_comma_from_isbn = second_split[0].replace(',', '')
        #    second_split[0] = remove_comma_from_isbn
        #    del second_split[2]
          
            print(row)
            #cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)", split_row)
            
    #sql = "COPY books1 FROM STDIN DELIMITER '|' CSV HEADER"
    #cur.copy_expert(sql, open('books.csv', "r+"))
    #cur.execute("INSERT INTO books (isbn, name, author, year) VALUES (%s, %s, %s, %s)")

conn.commit()

