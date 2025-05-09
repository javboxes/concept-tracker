# -*- coding: utf-8 -*-
"""Colab_rank_gn.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CaJhaZy-dQSmBMysTalC27-yxBzxOJmB
"""

import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import quote
from IPython.display import display, HTML

nest_asyncio.apply()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch Chromium in headless mode
        page = await browser.new_page()

        # Step 3: Set custom headers to mimic a real browser and avoid detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/"
        }

        # Set headers to the page
        await page.set_extra_http_headers(headers)

        # Step 4: Navigate to the page with concept fund flow data
        url = "https://data.10jqka.com.cn/funds/gnzjl/"
        await page.goto(url, wait_until="domcontentloaded", timeout=60000) # 60 秒

        # Step 5: Wait for the page to load completely
        # await page.wait_for_timeout(3000)

        # Step 6: Extract the page content
        content = await page.content()

        # Step 7: Use BeautifulSoup to parse the page (you can install beautifulsoup4 and lxml if needed)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        # Step 8: Extract top 10 concept fund flows from the table
        rows = soup.select("table.m-table.J-ajax-table tr")
        top_concepts = []
        print("概念资金流向（前10）")
        for idx, row in enumerate(rows[1:11], start=1):  # Skip header row
            cells = row.find_all("td")
            if len(cells) >= 4:
                name_cell = cells[1]
                name = cells[1].text.strip()
                name_encoded = quote(name)
                zdf = cells[3].text.strip()
                link = f"https://javboxes.com/catalogsearch/result/?order=sku&dir=desc&q={name_encoded} "

                top_concepts.append((name, zdf, link))

        # 构建 HTML 内容
        html_body = "<html><head><meta charset='utf-8'><title>概念涨跌幅前十</title></head><body></br></br>"
        for idx, (name, zdf, link) in enumerate(top_concepts, 1):
            html_body += f'<li style="font-size: 50px;">{idx}. <a href="{link}">{name}</a> - {zdf}</li>'
            html_body += "</ul></body></html>"

        display(HTML(html_body))

        # 保存为 HTML 文件
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_body)

        # Step 9: Close the browser
        await browser.close()

# 调用 async 函数时，确保在 asyncio.run() 中运行
if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run() 来执行 async main() 函数
