from discord import Member, VoiceState

from channelchat.commands.createchannel import create_channel
from channelchat.commands.deletechannel import delete_channel
from channelchat.config import config
from channelchat.events.dispatch import register
from channelchat.events.eventType import EventType


def empty_channel_count(before_channel, after_channel, current_channels):
    count = 0
    for channel in current_channels:
        if channel == before_channel:
            count += int(len(channel.members)-1 == 0)
        if channel == after_channel:
            count += int(len(channel.members)+1 == 0)
        else:
            count += int(len(channel.members) == 0)
    return count


async def remove_empty_channel(number_of_empty_channels, channel):
    if number_of_empty_channels > config.get_min_channels():
        await delete_channel(channel.guild, channel.category.name)


async def create_empty_channel_as_needed(number_of_empty_channels, channel, current_channels):
    if number_of_empty_channels > 0:
        return
    available_names = set(config.get_channel_names()) - set([channel.category.name for channel in current_channels])
    if len(available_names) == 0:
        return
    await create_channel(channel.guild, available_names.pop())


async def get_existing_channels(member):
    guild = member.guild
    channels = guild.categories
    channel_names = config.get_channel_names()
    return [channel.voice_channels[0] for channel in channels if channel.name in channel_names]


#@register(EventType.VOICE_STATE_UPDATE)
async def check_channel_supply(member: Member, before: VoiceState, after: VoiceState):
    """
    Dynamically creates and removes Channels as needed (keeps at least one free)
    """
    current_channels = await get_existing_channels(member)
    number_of_empty_channels = empty_channel_count(before.channel, after.channel, current_channels)
    #await remove_empty_channel(number_of_empty_channels, before.channel)
    #await create_empty_channel_as_needed(number_of_empty_channels, after.channel, current_channels)


