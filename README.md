# ChannelChat
Discord Textchannel for each Voicechannel. Works similar to Teamspeak chat.

Place a config.toml in the root directory of ChannelChat (the folder which contains setup.py).
config.toml example:
```
[main]
token = "YOUR__DISCORD_BOT_TOKEN"

[channel]
insert_position = WHERE_SHOULD_NEW_CHANNELS_SPAWN?
min_channels = HOW_MANY_EMPTY_CHANNELS_SHOUD_EXISTS?
role_prefix = "Channel: "
names = ["YOUR_FIRST_CHANNEL_NAME", "YOUR_SECOND_CHANNEL_NAME"]

[command]
prefix = '!'
history_length = 32

[log]
channel = "LOG_CHANNEL_ID"
```
