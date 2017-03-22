import json
import sqlite3
from TwitterAPI import TwitterAPI
api = TwitterAPI("gYaQqLlPplMjAuDWk5krCjV4W", "SbmqAT4XiVbvJ3pbDlkG15s4G9HzcRK2RVcDbXdoqi4ieDwO1X",
	"437803182-oC6F7n34TKPNgJ0hkEDSJ94ZDt1O2dcjKuYqbjpu", "vVagdZXd9S7czx6m5r4E4qmWiyreSMLRSIfnDnXv2ziUg")

r = api.request('search/tweets', {'q': '#twitterstorians'})
# for item in r:
# 	print(item)

# b = TwitterRestPager(api, 'search/tweets', {'q': '#twitterstorians', 'count': 100})



# for line in r:
#     try:
#         # Read in one line of the file, convert it into a json object 
#         tweet = json.loads(line.strip())
#         print(type(tweet))
#         if 'text' in tweet: # only messages contains 'text' field is a tweet
#             print(tweet['id']) # This is the tweet's id
#             print(tweet['created_at']) # when the tweet posted
#             print(tweet['text'])# content of the tweet
                        
#             # print tweet['user']['id'] # id of the user who posted the tweet
#             print(tweet['user']['name']) # name of the user, e.g. "Wei Xu"
#             print(tweet['user']['screen_name']) # name of the user account, e.g. "cocoweixu"
#     except:
#     	print('bad')
#     	continue

conn = sqlite3.connect('twitterstorians.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS tweets')
cur.execute('CREATE TABLE tweets(user TEXT, tweet TEXT)')

for item in r.get_iterator():
    user1 = item['user']['screen_name']
    tweet1 = item['text']
#    print(item['user']['screen_name'], item['text'])
    print(user1)
    cur.execute('INSERT INTO tweets (user, tweet) VALUES (?, ?)', (user1, tweet1))
    conn.commit()
