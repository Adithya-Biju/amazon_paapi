from utility.constant import LAST_RUN_PATH
import json
from datetime import datetime, timezone
import logging


def update_last_run_time():
    try:
        now_iso = datetime.now(timezone.utc).isoformat()
        with open(LAST_RUN_PATH, "w") as f:
            json.dump({"last_run": now_iso}, f)
        logging.info(f"✅ Date time updated ; {now_iso}.")
        
    except Exception as e:
        logging.error(f"Error update last_run.json: {e}")
