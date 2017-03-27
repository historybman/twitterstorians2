import json
import sqlite3
import TwitterAPI
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
cur.execute('CREATE TABLE tweets(user TEXT, tweet TEXT, date TEXT, mentions TEXT)')
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL, user TEXT UNIQUE, PRIMARY KEY(user_id))')

count = 0


for item in b.get_iterator():
    screen_namez = 0
    user1 = item['user']['screen_name']
    tweet1 = item['text']
    date1 = item['created_at']
    try:    
        #screen_name1 = item['entities']['user_mentions'][0]['screen_name']
        # try to treat the user mentions as a list and find the length
        screen_namez = len(item['entities']['user_mentions'])
        screen_name1 = []
        for i in range(screen_namez):
            tweeted = item['entities']['user_mentions'][i]['screen_name']
            screen_name1.append(tweeted)
            cur.execute('INSERT OR IGNORE INTO users (user) VALUES (?)', (tweeted, ))
            conn.commit()
    except:
        screen_name1 = []
    ## convert date
    date1 = datetime.datetime.strptime(date1, '%a %b %d %H:%M:%S +0000 %Y')
#    print(item['user']['screen_name'], item['text'])
    print(user1, date1, screen_name1, "screen_namez mentioned: ", screen_namez)
    #print(item['entities']['user_mentions'])
    screen_string = str(screen_name1)
    cur.execute('INSERT INTO tweets (user, tweet, date, mentions) VALUES (?, ?, ?, ?)', (user1, tweet1, date1, screen_string))
    conn.commit()
    cur.execute('INSERT OR IGNORE INTO users (user) VALUES (?)', (user1, ))
    conn.commit()
    count += 1
    print(count)
    if count < 200:
        continue
    else:
        break



#for item in b.get_iterator():
#    mentions = []
#    count2 = 0
#    if count < 200:    
#        try:
#            screen_name = item['entities']['user_mentions']['screen_name']
#            print(screen_name)
#            count += 1
#    #            mentions.append(screen_name)
#    #            count += 1
#    #            print(count2)
#    #            print(mentions)
#    #            print(item['user']['screen_name'])
#        except:
#            continue
# this current version will only take the first mention, not all of them. But let's see if it works.    
    
    
 
print('the end!')

## Next moves: use RE to parse twitter handles in tweets and add those to users
    # important to find out whether there's a way to do this within twitter api json
    
# Then make a third table which is contacts, which will store connections
# from tweeter to tweeted. 
# maybe isolate the retweets and do those separately
