import json
import sqlite3
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager
import datetime 
# insert API here



#r = api.request('search/tweets', {'q': '#twitterstorians'})
# for item in r:
# 	print(item)

b = TwitterRestPager(api, 'search/tweets', {'q': '#twitterstorians', 'count': 100})


conn = sqlite3.connect('twitterstorians.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS tweets')
cur.execute('CREATE TABLE tweets(user TEXT, tweet TEXT, date TEXT)')

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
    count += 1
    print(count)
    if count < 1500:
        continue
    else:
        break

 
print('the end!')
