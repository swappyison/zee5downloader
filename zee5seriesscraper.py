import requests

web_urls = []
url = input("enter show url: ")
url = url.strip()
url_parts = url.split('/')
content_id = url_parts[-1]  # Last part of the URL

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.zee5.com/',
    'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTEwLTI0VDEwOjMxOjU4LjQ2NVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5ODE0MzUxOH0.hKsRsKic5S9WENldti2HvuvZfDzHaZ7QXj6aTNH5GR0',
    'Origin': 'https://www.zee5.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
}

params = {
    'translation': 'en',
    'country': 'IN',
}

response = requests.get('https://gwapi.zee5.com/content/tvshow/' + content_id, params=params, headers=headers)
data = response.json()
items = data["seasons"]
for item in items:
    episodes = item.get("episodes")
    for episode in episodes:
        web_url = episode.get("web_url")
        web_urlz = f"https://www.zee5.com/{web_url}"
        print(web_urlz)
        web_urls.append(web_urlz)


with open('show_urls.txt', 'w') as file:
    for url in web_urls:
        file.write(f"{url}\n")