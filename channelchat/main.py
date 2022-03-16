#!/usr/bin/env python3
from collections import deque

from discord import VoiceState, Member
from configparser import ConfigParser
from discord.ext import commands
from discord.ext.commands import has_permissions

from channelchat.commands import createchannel, deletechannel
from channelchat.events import dispatch, handlers
from channelchat.events.eventType import EventType

config = ConfigParser()
config.read('../config.ini')
token = config.get('main', 'token')
log_channel = int(config.get('log', 'channel'))
command_history = deque(maxlen=32)
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    await dispatch.trigger(EventType.VOICE_STATE_UPDATE, member, before, after)


@bot.command()
async def create_channel(ctx, arg=None):
    await createchannel.create_channel(ctx, arg)

@bot.command()
async def delete_channel(ctx, arg=None):
    await deletechannel.delete_channel(ctx, arg)

@bot.command
async def undo(ctx, arg=None):
    await undo.undo(ctx, arg)


async def log(message: str):
    channel = bot.get_channel(log_channel)
    await channel.send(message)

bot.run(token)
