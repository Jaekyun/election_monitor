import requests
from bs4 import BeautifulSoup as bs
import telegram
import asyncio

async def get_new_links(old_links=[]):
    url = f'https://search.naver.com/search.naver?where=news&query=%EA%B5%AD%EB%AF%BC%EC%9D%98%ED%9E%98%20%7C%20%EC%9D%B4%EC%A4%80%EC%84%9D%20%7C%20%EC%A3%BC%EC%A7%84%EC%9A%B0%20%7C%20%5B%EB%8B%A8%EB%8F%85%5D%20%7C%20%ED%9B%84%EB%B3%B4%20%7C%20%EC%B6%9C%EB%A7%88%20%2B%EC%B4%9D%EC%84%A0&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_titles = soup.select('a.news_tit')
    list_links = [i.attrs['href'] for i in news_titles]

    new_links = [link for link in list_links if link not in old_links]

    return new_links

async def send_links(bot, chat_id):
    global old_links

    new_links = await get_new_links(old_links)

    if new_links:
        # Reverse the order of new links to send the most recent news first
        new_links.reverse()

        for link in new_links:
            await bot.send_message(chat_id=chat_id, text=link)
    else:
        pass

    old_links += new_links.copy()

async def periodic_task(bot, chat_id):
    while True:
        await send_links(bot, chat_id)
        await asyncio.sleep(5)  # Execute every 5 seconds

async def main():
    bot_token = '5139194628:AAHB_PXqv0y_xfn57Z5IAAYL98QtxPLn7-o'
    bot = telegram.Bot(token=bot_token)

    chat_id = '@eyes1000'

    await bot.send_message(chat_id='@eyes1000', text="국민의힘 | 이준석 | 주진우 | [단독] | 후보 | 출마 +총선 키워드 뉴스 검색")

    global old_links
    old_links = []

    task = asyncio.ensure_future(periodic_task(bot, chat_id))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        task.cancel()

if __name__ == '__main__':
    asyncio.run(main())
