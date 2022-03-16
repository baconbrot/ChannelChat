from discord.ext.commands import has_permissions
from channelchat.main import command_history, bot

async def undo(ctx):
    if len(command_history) == 0:
        return
