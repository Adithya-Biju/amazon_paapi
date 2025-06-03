from utility.constant import LAST_RUN_PATH
import json
from datetime import datetime, UTC
import logging


def update_last_run_time():

    try:
        with open(LAST_RUN_PATH, "w") as f:
            json.dump({"last_run": datetime.now(UTC).isoformat()}, f)
            logging.info(f"✅ Date time updated ; {datetime.now(UTC).isoformat()}.")
        
    except Exception as e:
        logging.error(f"Error update last_run.json: {e}")