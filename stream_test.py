import json
import sqlite3
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager
import datetime 
from api import api


#r = api.request('search/tweets', {'q': '#twitterstorians'})
# for item in r:
# 	print(item)

b = TwitterRestPager(api, 'search/tweets', {'q': '#twitterstorians', 'count': 100})


conn = sqlite3.connect('twitterstorians.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS tweets')
cur.execute('CREATE TABLE tweets(user TEXT, tweet TEXT, date TEXT)')
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL, user TEXT UNIQUE, PRIMARY KEY(user_id))')

count = 0


for item in b.get_iterator():
    user1 = item['user']['screen_name']
    tweet1 = item['text']
    date1 = item['created_at']
    ## convert date
    date1 = datetime.datetime.strptime(date1, '%a %b %d %H:%M:%S +0000 %Y')
#    print(item['user']['screen_name'], item['text'])
    print(user1, date1)
    cur.execute('INSERT INTO tweets (user, tweet, date) VALUES (?, ?, ?)', (user1, tweet1, date1))
    conn.commit()
    cur.execute('INSERT OR IGNORE INTO users (user) VALUES (?)', (user1, ))
    conn.commit()
    count += 1
    print(count)
    if count < 200:
        continue
    else:
        break

 
print('the end!')
