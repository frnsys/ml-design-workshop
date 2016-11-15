import json
import time
from dateutil.parser import parse

d = json.load(open('articles.json', 'r'))

def process_article(a):
    created_at = parse(a['created_at'])
    created_at = time.mktime(created_at.timetuple())
    return {
        'created_at': created_at,
        'url': a['url'],
        'title': a['title'],
        'image': a['image'],
        'text': a['text'],
        'summary': a['summary']
    }

articles = [process_article(a) for a in d]

with open('articles_processed.json', 'w') as f:
    json.dump(articles, f)