import json
import time
from dateutil.parser import parse

d = json.load(open('articles.json', 'r'))

seen_titles = set()
to_remove = [
    'recipe', 'nfl', 'ufc', 'car', 'vehicle',
    'musical', 'cubs', 'football', 'quarterback',
    'fashion', 'baseball', 'restaurants', 'restaurant',
    'basketball', 'warriors', 'game', 'nba', 'sport',
    'volkswagen', 'jaguar', 'food', 'tv', 'music',
    'photographers', 'halloween', 'art', 'bears', 'permalink',
    'soccer', 'films', 'thanksgiving', 'forecast', 'hbo', 'quiz',
    'polo', 'tennis', 'series', 'inferno', 'disney', 'beachy',
    'outfit', 'memoir', 'supermoon'
]

def process_article(a):
    created_at = parse(a['created_at'])
    created_at = time.mktime(created_at.timetuple())
    return {
        'created_at': created_at,
        'url': a['url'],
        'title': a['title'],
        'image': a['image'],
        'text': a['text'],
        'summary': a['summary'],
        'keywords': a['keywords']
    }

def keep(a):
    """removes duplicates and articles containing skipped keywords"""
    seen = a['title'] in seen_titles
    if not seen:
        seen_titles.add(a['title'])
    return not (set(to_remove) & set(a['keywords'])) and not seen

articles = [process_article(a) for a in d if keep(a)]

# from collections import defaultdict
# words = defaultdict(int)
# for a in articles:
#     for kw in a['keywords']:
#         words[kw] += 1

# sortkws = sorted(words.items(), key=lambda i: i[1])
# for k, n in sortkws:
#     print(k, n)
# print('---')

print('removed {}'.format(len(d) - len(articles)))
print('remains {}'.format(len(articles)))
with open('articles_processed.json', 'w') as f:
    json.dump(articles, f)