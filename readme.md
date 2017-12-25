# Delete Discord History

This script deletes all the user's history in the selected channels.

## Retrieve User and Channel Tokens

To retrieve your user token, open the discord webui while logged in, open Inspector with F12, click the Application tab. Under the Storage tree in the left column, select Local Storage > https://discordapp.com. Search for ```token``` and copy the value.

To get the channel IDs, go to the channel you want to delete, copy the last portion of the url which should be in the format https://discordapp.com/channels/```<server id>```/```<channel id>```

## Configure

Copy sample.json and rename to info.json. Enter your username, user token, and channel IDs in the empty fields. Channels is a list of channel IDs.

## Run

```
$ python main.py
```

### Note

The script adds a delay of 0.3s between deletions to avoid rate limiting by discord. It's recommended that this script be run in the background with screen/tmux.

## Authors

* [Imad Mouhtassem](https://github.com/mouhtasi) - Python 3 migration. Ease of use
* [Will Ingarfield](https://github.com/elevenchars) - Initial work