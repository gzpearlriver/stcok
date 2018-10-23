import pandas as pd
import sqlite3 as lite
import tushare as ts


db_file = 'd:\\stockdata\\stock.db'

conn=lite.connect(db_file)
cur = conn.cursor()

sql = "select * from stocklist"
oldlist = pd.read_sql_query(sql, conn)

newlist = ts.get_stock_basics()
newlist['name'] = newlist['name'].str.replace('*','')
newlist['name'] = newlist['name'].str.replace(' ','')
newlist = newlist.reset_index()
#把code从Index转为列
oldlist['code'] = oldlist['code'].astype(str)
oldlist['code'] = oldlist['code'].str.zfill(6)

delta_n_o = set(newlist['code']) - set(oldlist['code'])
print("new - old")
print(delta_n_o)

delta_o_n = set(oldlist['code']) - set(newlist['code'])
print("old - new")
print(delta_o_n)

cur.execute('alter table stocklist rename to stocklist_old;')
newlist.to_sql('stocklist', con=conn, if_exists='append')
