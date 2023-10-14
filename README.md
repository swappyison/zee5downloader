
# Zee5 Downloader ⬇

✅ Download both DRM and DRM free videos from Zee5

📒NOTE: Please move all scripts inside WKS-KEYS folder before doing anything.

📒 NOTE: Premium content can be downloaded with a premium account.

## 🎯Features

🔥 4k support

🔈 Multi-audio

💬 Subtitle download

⏩ High speed
## Steps

1.Clone the repo:
```javascript
git clone https://github.com/swappyison/zee5downloader.git
```
2.Install required dependencies 
```javascript
pip3 install -r requirements.txt
```

3.First you need to scrape the urls, run python script in terminal: 
```javascript
python3 zee5urlscraper.py
```
It will ask for two values, for base url:

   ![SCR-20230901-j79](https://github.com/swappyison/zee5downloader/assets/88504971/47ae7ff9-24b6-4983-b540-1edfeb177fed)

📒 NOTE: Please see the url above, here i typed **gwapi** under network tab of developer tools and found a url that looked like above, it needs to have page limit at end and season id in the url.

then i found access token, by scrolling down.

   ![SCR-20230901-j5r](https://github.com/swappyison/zee5downloader/assets/88504971/0cd62294-c481-493a-b642-c6662d7c6466)

This should execute the script and it will search for all urls and scrape them to shows_url.txt file

4.Now run:
```javascript
python3 zee5improv.py
        OR
python3 zee4k.py
```
zeeimprov.py will bulk download 1080p shows and zee4k will do the same for 4k supported shows.

## Note 📒

Authorization token, x-access-token and x-dd-token expire after some time, you can grab a fresh pair as seen below:
![SCR-20230901-ocf](https://github.com/swappyison/zee5downloader/assets/88504971/5631a4ed-a7f3-4ebf-9bc1-d492b6f0ae75)

Note: Just run zee5.sh(for linux/mac) or zee5.bat(windows) to execute everything at once.
Update: the above method is for downloading shows, for downloading movies use zeemovie.py script.

