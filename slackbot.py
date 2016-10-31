import re
import json
import time
import config
from slackclient import SlackClient

# how many most recent news results to show
N_RESULTS=5

stories = json.load(open('data.json', 'r'))

all_events = []
for story in stories:
    all_events += story['events']
all_events = sorted(all_events, key=lambda e: min(a['created_at'] for a in e['articles']))

def get_news(matches):
    """just grab first article for each event"""
    news = all_events[:N_RESULTS]
    return 'Here\'s the latest news:\n- {}'.format(
        '\n- '.join([e['articles'][0]['title'] for e in news]))

def get_more(matches):
    """this is sloppy"""
    result = None
    query = matches[1]
    evs = all_events[:N_RESULTS]

    # brute-force search the most recent news for one
    # that mentions the query
    titles = [e['articles'][0]['title'].lower() for e in evs]
    for i, title in enumerate(titles):
        if query in title:
            result = i
            break

    if result is None:
        return "I don't know what you're talking about?"

    else:
        ev = evs[i]
        article = ev['articles'][0]
        story_id = ev['story_id']
        other_events = [e['articles'][0] for e in stories[story_id]['events']]
        return '*{}* (<{}>)\n{}\n{}\n\nOther events in this story:\n- {}'.format(
            article['title'],
            article['url'],
            article['text'].split('\n')[0],
            article['image'],
            '\n- '.join([a['title'] for a in other_events])
        )


commands = {
    '(hello|hi|hey)!?': 'hi there!',
    'what\'s new?': get_news,
    'tell me (more )?about (.+)': get_more
}

# compile regexes
commands = {re.compile(k): v for k, v in commands.items()}

def parse_command(cmd, msg):
    """given a command (regex),
    see if this message matches it"""
    match = cmd.match(msg)
    if match is None:
        return False
    else:
        return match.groups()

id = None
sc = SlackClient(config.TOKEN)
if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        for ev in events:
            # get the bot's own user id
            if id is None and ev['type'] == 'presence_change':
                id = ev['user']

            # respond to a user msg
            if ev['type'] == 'message' and 'user' in ev and ev['user'] != id:
                # convert to lowercase for consistency
                msg = ev['text'].lower()
                response = None

                # brute-force search for a response
                for reg, resp in commands.items():
                    matches = parse_command(reg, msg)
                    if matches is False:
                        continue
                    else:
                        response = resp(matches) if callable(resp) else resp
                        break

                # default response
                if response is None:
                    response = "I don't know what to say..."

                # send the response to the channel
                sc.api_call('chat.postMessage',
                            channel=ev['channel'],
                            text=response,
                            as_user=True)
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")