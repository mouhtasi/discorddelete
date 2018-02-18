import json
import requests
import time

print("In order for this script to work, the channel ids, auth token, and username are required in the info.json file")

with open('info.json', 'r') as f:
    info = json.load(f)

username = info['username']
auth_token = info['auth_token']
channels = info['channels']


def get_all_user_messages(auth_token, channel_id):
    all_messages = []
    num_of_returned_messages = 100
    last_message_id = ''
    while num_of_returned_messages == 100:
        messages = get_100_messages(auth_token, channel_id, last_message_id)  # get 100 messages
        if messages:
            # last_message_id = min(messages, key=lambda x: x['timestamp'])
            last_message = sorted(messages, key=lambda x: x['timestamp'], reverse=True)[-1]  # get the last message
            last_message_id = last_message['id']
            print('Downloading messages... {}'.format(last_message['timestamp']), end='\r')
            filtered_messages = [m for m in messages if m['author']['username'] == username]  # filter for user's messages
            all_messages += filtered_messages  # add these messages to the list
            num_of_returned_messages = len(messages)  # count how many messages we got this time
    return all_messages


def get_100_messages(auth, id, last=''):
    if not last:  # first method call, start from beginning (might be able to remove)
        messages = json.loads(requests.get("http://discordapp.com/api/v6/channels/" + id + "/messages",
                                           headers={"authorization": auth},
                                           params={"limit": 100}).content)
    else:
        messages = json.loads(requests.get("http://discordapp.com/api/v6/channels/" + id + "/messages",
                                           headers={"authorization": auth},
                                           params={"before": last, "limit": 100}).content)

    return messages


def delete_messages(auth, id, user, messages):
    print("deleting all messages in {} from username {}".format(id, user))
    for message in messages:
        print(message['content'])
        requests.delete("http://discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"],
                        headers={"authorization": auth})
        time.sleep(0.2)  # avoid rate limiting
    print("all messages deleted")


if __name__ == '__main__':
    for channel_id in channels:
        user_messages = get_all_user_messages(auth_token, channel_id)
        delete_messages(auth_token, channel_id, username, user_messages)
