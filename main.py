import mysql.connector
from query import sql
import config

import os

print(os.path.abspath('main.py'))



def printMd(fd, title, rows, values):
    fd.write("####"+title+"\n")
    #rows
    fd.write("|")
    row_nums = len(rows)
    for row in rows:
        fd.write(row+"|")
    fd.write("\n")
    #table
    fd.write("|")
    for row in range(row_nums):
        fd.write("---|")
    fd.write("\n")
    #lines
    for line in values:
        fd.write("|")
        for unit in line:
            fd.write(str(unit)+"|")
        fd.write("\n")

if __name__ == '__main__':
    db = mysql.connector.connect(
        host=config.host,
        user=config.user,
        port=config.port,
        passwd=config.passwd,
        database=config.database,
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()
    fd = open("./query_output.md", "w")
    for pir in sql:
        #fd.write(pir[0]+"\n")
        is_multi = pir[1].count(';')>1
        for result in cursor.execute(pir[1], multi=True):
            if result.with_rows:
                values = cursor.fetchall()
                rows = cursor.column_names
                printMd(fd, pir[0], rows, values)
                break
        fd.write("\n")
    fd.close()
    cursor.close()
    db.close()

    #check
    with open("./query_output.md", "r") as fd:
        lines = fd.readlines()
        for line in lines:
            print(line,end="")

