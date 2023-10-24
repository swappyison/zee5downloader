
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
It will ask for two values, for base url follow link like:

https://gwapi.zee5.com/content/tvshow/?season_id=0-2-KundaliBhagya1&type=episode&translation=en&country=IN&on_air=true&asset_subtype=tvshow&page=0&limit=10


📒 NOTE: Please see the url above, here i typed **gwapi** under network tab of developer tools and found a url that looked like above, it needs to have page limit at end and season id in the url.

then i found access token, by scrolling down.

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
https://spapi.zee5.com/singlePlayback/v2/displayAds?state=UT&country=IN&platform_name=desktop_web&user_type=free.....

if you need latest shows that has mpd that starts with: v2-prime then use zee5latestdownloader.py 
for paid series use zee5seriesscraper.py
