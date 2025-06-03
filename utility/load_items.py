import json
from utility.constant import ITEMS_LIST 
import logging

def load_items_from_json():

    if ITEMS_LIST.exists():
            try:
                with open(ITEMS_LIST, "r") as f:
                        items = json.load(f)
                        return items
                
            except Exception as e:
                logging.error(f"Error read items.json: {e}")

    return None