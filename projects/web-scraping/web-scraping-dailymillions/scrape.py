from bs4 import BeautifulSoup
from csv import writer
import re
import requests
import os

urls = ["https://www.irishlottery.com/daily-million-archive-2016",
        "https://www.irishlottery.com/daily-million-archive-2017",
        "https://www.irishlottery.com/daily-million-archive-2018",
        "https://www.irishlottery.com/daily-million-archive-2019",
        "https://www.irishlottery.com/daily-million-archive-2020",
        "https://www.irishlottery.com/daily-million-archive-2021",
        "https://www.irishlottery.com/daily-million-archive-2022",
        "https://www.irishlottery.com/daily-million-archive-2023"]

for url in urls:
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        file_exists = os.path.exists('daily_million.csv')
        info = []

        with open("daily_million.csv", "a", encoding="utf-8") as csvfile:
            writer_csv = writer(csvfile)
            if not file_exists:
                writer_csv.writerow(["date", "day", "month", "year", "ball1", "ball2", "ball3", "ball4", "ball5", "ball6", "bonus"])

            table = soup.find("table")
            for tr in table.findAll("tr"):
                for th in tr.findAll("th"):
                    date = re.sub(r'([\t\r\n])', '', th.text)
                    day = re.search(r"[0-9]+(?:st|[nr]d|th)", date)
                    month = re.search(r'\w\w\w', date)
                    year = re.search(r'\d{4}', date)
                    for ul in tr.findAll("ul"):
                        ball = [int(s) for s in ul.text.split() if s.isdigit()]
                        info = [date, day.group(), month.group(), year.group(), ball[0], ball[1], ball[2], ball[3], ball[4], ball[5], ball[6]]
                        writer_csv.writerow(info)
                    print(info)
    except Exception:
        continue
