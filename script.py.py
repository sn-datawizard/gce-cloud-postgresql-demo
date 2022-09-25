import pandas as pd
import psycopg2
import sqlalchemy

con = psycopg2.connect(host=<databaseIP>, database="postgres", user=<user>, password=<password>)
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

engine = sqlalchemy.create_engine('postgresql+psycopg2://<user>:<password>@<databaseIP>/postgres')
print(engine)
df.to_sql(name='table1', con=engine, if_exists='replace', index=False)

