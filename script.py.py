import pandas as pd
import psycopg2
import sqlalchemy

con = psycopg2.connect(host='34.159.54.139', database="postgres", user="postgres", password="admin")
print(con)
cursor = con.cursor()
try:
    cursor.execute("""CREATE TABLE table1 (Country CHAR(50), ItemType CHAR(50), UnitsSold INT)""")
except:
    print('Table already exists')
con.commit()
con.close()
cursor.close()

df = pd.read_csv('./data.csv', sep=';', index_col=False)
print(df.head(5))

engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:admin@34.159.54.139/postgres')
print(engine)
df.to_sql(name='table1', con=engine, if_exists='replace', index=False)

