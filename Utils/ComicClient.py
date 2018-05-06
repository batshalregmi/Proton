import random
import datetime
from bs4 import BeautifulSoup
import functools


class ComicClient:

    def __init__(self, bot):
        self.bot = bot
        self.dilbertURL = "http://www.dilbert.com/strip/"
        self.garfieldURL = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield"

    def getDilbertDate(self, mode):
        if mode == 0:
            year = random.randint(1990, datetime.date.today().year)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            return f"{self.dilbertURL}{year}-{month}-{day}"
        else:
            today = datetime.date.today()
            return f"{self.dilbertURL}{today.year}-{today.month}-{today.day}"

    def parseDilbertHTML(self, html):
        soup = BeautifulSoup(html, "lxml")
        comicRoot = soup.find_all(attrs={"class": "img-comic"})
        comicRoot = comicRoot[0]["src"]
        return comicRoot

    async def getDilbert(self, mode):
        """Get a Dilbert comic, from the official website."""
        func = functools.partial(self.getDilbertDate, mode)
        url = await self.bot.loop.run_in_executor(None, func)
        async with self.bot.session.get(url) as resp:
            html = await resp.text()
        func = functools.partial(self.parseDilbertHTML, html)
        url = await self.bot.loop.run_in_executor(None, func)
        return url

    def getGarfieldDate(self, mode):
        if mode == 0:
            year = random.randint(1979, datetime.date.today().year)
            month = random.randint(1, 12)
            if month < 10:
                month = f"0{month}"
            day = random.randint(1, 28)
            if day < 10:
                day = f"0{day}"
            print(day, month)
            return f"{self.garfieldURL}/{year}/{year}-{month}-{day}.gif"
        else:
            today = datetime.date.today()
            month = today.month
            day = today.day
            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"
            print(day, month)
            return f"{self.garfieldURL}/{today.year}/{today.year}-{month}-{day}.gif"

    async def getGarfield(self, mode):
        """Get a Garfield comic."""
        func = functools.partial(self.getGarfieldDate, mode)
        url = await self.bot.loop.run_in_executor(None, func)
        return url

        
            
        

