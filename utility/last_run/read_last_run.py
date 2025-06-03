from utility.constant import LAST_RUN_PATH, INTERVAL_HOURS
import json
from datetime import datetime, UTC, timedelta
import logging 


def get_last_run_time():

    if LAST_RUN_PATH.exists():
        try:
            with open(LAST_RUN_PATH, "r") as f:
                    data = json.load(f)
                    last_run =  datetime.fromisoformat(data["last_run"])
                    return datetime.now(UTC) - last_run >= timedelta(hours=INTERVAL_HOURS)
            
        except Exception as e:
            logging.error(f"Error read last_run.json: {e}")

    return None