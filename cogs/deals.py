import discord
from discord.ext import commands, tasks
import settings
import logging
from utility import get_last_run_time, update_last_run_time
from service import find_deals

class DealsCog(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
        self.check_and_run_deals.start()


    async def cog_unload(self):
        self.check_and_run_deals.cancel()


    @tasks.loop(minutes=10)
    async def check_and_run_deals(self):

        if get_last_run_time() == False:
            return

        logging.info("✅ Time to run deal fetcher.")

        await find_deals(self.bot)

        update_last_run_time()


async def setup(bot):
        await bot.add_cog(DealsCog(bot),guilds = [discord.Object(id=settings.GUILD_ID)])