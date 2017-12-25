import json
import requests
import time

print("In order for this script to work, the channel ids, auth token, and username are required in the info.json file")

with open('info.json', 'r') as f:
    info = json.load(f)

username = info['username']
auth_token = info['auth_token']
channels = info['channels']

delete_from_all_users = True if input("delete messages from other users (y/n): ") == "y" else False


def get_all_messages(auth, id, last="", prev=[]):  # recursively find all messages in a channel, 100 at a time
    if not last:  # first method call, start from beginning (might be able to remove)
        messages = json.loads(requests.get("http://discordapp.com/api/v6/channels/" + id + "/messages",
                                           headers={"authorization": auth},
                                           params={"limit": 100}).content)
    else:
        messages = json.loads(requests.get("http://discordapp.com/api/v6/channels/" + id + "/messages",
                                           headers={"authorization": auth},
                                           params={"before": last, "limit": 100}).content)

    prev = prev + messages

    if len(messages) < 100:
        print("got to end of channel at " + str(len(prev)) + " messages")
        return prev
    else:
        oldest = sorted(messages, key=lambda x: x["timestamp"], reverse=True)[-1]
        return get_all_messages(auth, id, last=oldest["id"], prev=prev)


def delete_all(auth, id, user, messages):
    print("deleting all messages in {} from username {}".format(id, user))
    for message in messages:
        if delete_from_all_users:
            requests.delete("http://discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"],
                            headers={"authorization": auth})
            time.sleep(0.2)  # avoid rate limiting

        else:
            if message["author"]["username"] == user:
                print(message['content'])
                requests.delete("http://discordapp.com/api/v6/channels/" + id + "/messages/" + message["id"],
                                headers={"authorization": auth})
                time.sleep(0.2)  # avoid rate limiting
    print("all messages deleted")


for channel_id in channels:
    delete_all(auth_token, channel_id, username, get_all_messages(auth_token, channel_id))
