import psycopg2

conn = psycopg2.connect(database="testeDB",
                        host="localhost",
                        user="user",
                        password="password",
                        port="5434")

conn.autocommit = True
cursor = conn.cursor()

with open('init.sql','r') as arq:
    script=arq.read()
    print(script)
    cursor.execute(script)

cursor.close()
conn.close()
