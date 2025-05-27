import discord
from discord.ext import commands
import settings

class DealsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_deals.start()



async def setup(bot):
        await bot.add_cog(DealsCog(bot),guilds = [discord.Object(id=settings.GUILD_ID)])