import getopt
import logging
import sys
import toml


try:

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for opt, arg in opts:
        if opt == '-c':
            config_path = arg

except:
    config_path = 'config.toml'
else:
    config_path = 'config.toml'
logging.info(f"Config path: {config_path}")
config = toml.load(config_path)


def get_token():
    token = config.get('main').get('token')
    return token


def get_channel_names():
    channel_names = config.get('channel').get('names')
    return list(channel_names)


def get_channel_insert_position():
    channel_insert_position = config.get('channel').get('insert_position')
    return channel_insert_position


def get_log_channel():
    log_channel = config.get('log').get('channel')
    return log_channel


def add_channel_name(name: str):
    global config
    channels_config = config.get('channel')
    channel_names = channels_config.get('names')
    if name.lower() in [channel_name.lower() for channel_name in channel_names]:
        return
    channel_names.append(name)
    config['channel']['names'] = channel_names
    with open(config_path, 'w') as f:
        toml.dump(config, f)


def get_command_prefix():
    global config
    prefix = config.get('command').get('prefix')
    return prefix


def get_command_history_length():
    global config
    length = config.get('command').get('history_length')
    return length


def get_channel_role_prefix():
    global config
    prefix = config.get('channel').get('role_prefix')
    return prefix


def get_min_channels():
    global config
    count = config.get('channel').get('min_channels')
    return count
