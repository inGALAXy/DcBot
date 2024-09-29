import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

class stream(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    @commands.command()
    async def typhoon(self, ctx: commands.Context):
        # 发送HTTP请求获取网页内容
        url = "https://www.dgpa.gov.tw/typh/daily/nds.html"
        response = requests.get(url)
        response.encoding = "utf-8"  # 设置网页内容的编码方式
        html_content = response.text

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_content, "html.parser")

        # 找到所有的行
        rows = soup.find_all("tr")

        # 遍歷每一行並提取縣市名稱和停課資訊
        for row in rows:
            # 檢查是否有 <h2> 標籤，且內容是否為 '無停班停課訊息。'
            h2_tag = row.find('h2')
            if h2_tag and "無停班停課訊息" in h2_tag.text:
                await ctx.send("無停班停課訊息")
                break  # 找到後退出循環

            # 繼續查找停課訊息的其他行
            columns = row.find_all("td")
            if len(columns) == 2:  # 確保行中有兩列（縣市名稱和停課資訊）
                city_name = columns[0].text.strip()  # 提取縣市名稱並去除首尾空格
                stop_info = columns[1].text.strip()  # 提取停課資訊並去除首尾空格
                await ctx.send(f"縣市名稱: {city_name}, 停課資訊: {stop_info}")


    
   

async def setup(bot):
    await bot.add_cog(stream(bot))