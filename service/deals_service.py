from utility.paapi_search_items import search_items
import discord
from discord.ext import commands
import settings
from utility import constant
import asyncio
import logging
from utility import load_items_from_json


async def find_deals(bot: commands.Bot):

    items = load_items_from_json()

    for channel_id, keywords in items.items():

        target_channel = bot.get_channel(int(channel_id))
        
        if target_channel is None:
            logging.warning(f"Channel '{target_channel}' not found.")
            continue


        for keyword in keywords:

            try:
                results = await search_items(keyword)
                await asyncio.sleep(1)

                if not results:
                    logging.warning(f"No items found for keyword: {keyword}")
                    break

                for deal in results:
                    embed = discord.Embed(
                        title=results[deal]['item_title'],
                        url=results[deal]['item_url'],
                        description=f"💸 **Price**: {results[deal]['item_price']}\n🔥 **Discount**: {results[deal]['item_discount']}% OFF"
                    )
                    if results[deal]["items_img"]:
                        embed.set_image(url=results[deal]["items_img"])

                    await target_channel.send(embed=embed)
                    # await asyncio.sleep(1)

            except Exception as e:
                logging.error(f"❌ Error fetching deals for '{keyword}': {e}")