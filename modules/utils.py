import pandas as pd
import re
from datetime import datetime

def week_sort_key(week_str: str) -> pd.Timestamp:
    """
    ใช้สำหรับการเรียงลำดับสัปดาห์
    ตัวอย่าง week_str: "Week of 01-07 July 2024"
    """
    m = re.search(r'(\d{2})-(\d{2}) (\w+) (\d{4})', week_str)
    if m:
        day1, day2, month, year = m.groups()
        try:
            dt = pd.to_datetime(f"{day1} {month} {year}", format="%d %B %Y")
            return dt
        except:
            return pd.NaT
    return pd.NaT

def get_current_time() -> str:
    """
    คืนค่าวันที่และเวลาปัจจุบัน
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
