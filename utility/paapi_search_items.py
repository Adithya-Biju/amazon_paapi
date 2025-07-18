from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException
import json
import asyncio
import settings
from utility import constant


async def search_items(keyword):

    access_key = settings.ACCESS_KEY

    secret_key = settings.SECRET_KEY

    partner_tag = constant.REF_CODE

    host = constant.HOST
    region = constant.REGION

    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    search_index = "All"

    item_count = 10

    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
        SearchItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
        SearchItemsResource.IMAGES_PRIMARY_MEDIUM
    ]

    amazon_discounts = []
    unique_amazon_discounts = {}

    for i in range(1,5):

        try:
            search_items_request = SearchItemsRequest(
                partner_tag=partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                keywords=keyword,
                search_index=search_index,
                item_count=item_count,
                item_page=i,
                resources=search_items_resource,
                marketplace="www.amazon.sa"
            )

            await asyncio.sleep(1)

        except ValueError as exception:
            print("Error in forming SearchItemsRequest: ", exception)
            return

        try:
            """ Sending request """
            response = default_api.search_items(search_items_request)

            for item in response.search_result.items:
            
                    try:

                        amazon_discounts.append(
                            {"item_url":item.detail_page_url,
                            "items_img":item.images.primary.medium.url,
                            "item_title": item.item_info.title.display_value,
                            "item_price": item.offers.listings[0].price.amount,
                            "item_discount": item.offers.listings[0].price.savings.percentage
                            }
                            )

                    except:
                        pass

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)

    for item in amazon_discounts:
        unique_amazon_discounts[item['item_url']] = item

    return unique_amazon_discounts