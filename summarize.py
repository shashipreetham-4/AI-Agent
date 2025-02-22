import psycopg2

conn = psycopg2.connect(
    dbname="news_db",
    user="postgres",
    password="Shashi@21926",
    host="localhost",
    port="5432"
)
print("✅ PostgreSQL Connected Successfully!")

conn.close()
