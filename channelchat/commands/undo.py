from discord.ext.commands import has_permissions
from channelchat.main import command_history, bot


@bot.command
@has_permissions(manage_channels=True, manage_roles=True)
async def undo(ctx):
    if len(command_history) == 0:
        return
