import discord
from discord import VoiceState, Member
from discord.utils import get
import os

from discord.ext import commands

TOKEN = 'YOUR_TOKEN'

client = discord.Client()
bot = commands.Bot(command_prefix='!')

def get_channel_role(voiceState: VoiceState):
    return 'Channel: ' + voiceState.channel.category.name

@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    # Unsubscribe before text-channel
    try:
        old_role = discord.utils.get(member.guild.roles, name=get_channel_role(before))
        await member.remove_roles(old_role)
    except Exception as e:
        print(e)
    # Subscribe to after text-channel
    try:
        new_role = discord.utils.get(member.guild.roles, name=get_channel_role(after))
        await member.add_roles(new_role)
    except Exception as e:
        print(e)



client.run(TOKEN)
