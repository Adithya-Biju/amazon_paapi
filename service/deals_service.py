from amazon_paapi import AmazonApi
import discord
from discord.ext import commands
import settings
from utility import constant
import asyncio
import logging
from utility import load_items_from_json

amazon = AmazonApi(
    settings.ACCESS_KEY,
    settings.SECRET_KEY,
    constant.REF_CODE,
    country="SA"
)


async def find_deals(bot: commands.Bot):

    items = load_items_from_json()

    for target_channel, keywords in items.items():

        target_channel = discord.utils.get(bot.get_all_channels(), name=target_channel)
        if target_channel is None:
            logging.warning(f"❌ Channel '{target_channel}' not found.")
            continue

        for keyword in keywords:

            try:
                results = amazon.search_items(
                    keywords=keyword,
                    item_count=10
                )

                if not results.items:
                    logging.warning(f"No items found for keyword: {keyword}")
                    break

                top_discounted = []

                for item in results.items:
                    
                    try:
                        listing = item.offers.listings[0]
                        price = listing.price.amount
                        highest_price = item.offers.summaries[0].highest_price.amount
                        discount = (highest_price - price) / highest_price

                        if discount < 0.10:
                            continue

                        top_discounted.append({
                            "title": item.item_info.title.display_value,
                            "price": listing.price.display_amount,
                            "discount_pct": round(discount * 100),
                            "link": item.detail_page_url,
                            "image": item.images.primary.medium.url
                        })

                    except Exception as e:
                        logging.warning(f"⚠️ Skipping item due to missing data: {e}")
                        continue

                top_discounted = sorted(top_discounted, key=lambda d: d["discount_pct"], reverse=True)[:10]

                for deal in top_discounted:
                    embed = discord.Embed(
                        title=deal['title'],
                        url=deal["link"],
                        description=f"💸 **Price**: {deal['price']}\n🔥 **Discount**: {deal['discount_pct']}% OFF"
                    )
                    if deal["image"]:
                        embed.set_image(url=deal["image"])

                    await target_channel.send(embed=embed)
                    await asyncio.sleep(1)

            except Exception as e:
                logging.error(f"❌ Error fetching deals for '{keyword}': {e}")
