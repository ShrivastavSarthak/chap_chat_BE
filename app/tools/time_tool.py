from datetime import datetime, timezone
import json


async def get_current_time(timezone_name:str = "UTC")->str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return json.dumps({"timezone":timezone_name, "current_time":now})