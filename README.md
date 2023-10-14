#Zee5 Downloader ⬇

✅ Download both DRM and DRM free videos from Zee5

📒NOTE: Please move all scripts inside WKS-KEYS folder before doing anything.
🎯Features

🔥 4k support

🔈 Multi-audio

💬 Subtitle download

⏩ High speed

💲 Premium videos access
Steps

1.Clone the repo:

git clone https://github.com/swappyison/zee5downloader.git

2.Install required dependencies

pip3 install -r requirements.txt

3.Edit the .env file and place your token values

4.First you need to scrape the urls, run python script in terminal:

python3 zee5urlscraper.py

It will ask for two values, for base url:

SCR-20230901-j79

📒 NOTE: Please see the url above, here i typed gwapi under network tab of developer tools and found a url that looked like above, it needs to have page limit at end and season id in the url.

then i found access token, by scrolling down.

SCR-20230901-j5r

This should execute the script and it will search for all urls and scrape them to shows_url.txt file

4.Now run:

python3 zee5improv.py
        OR
python3 zee4k.py

zeeimprov.py will bulk download 1080p shows and zee4k will do the same for 4k supported shows.

image https://www.youtube.com/watch?v=yWwpPZ7zW4A&ab_channel=swapnilupadhyay
Note 📒

Authorization token, x-access-token and x-dd-token expire after some time, you can grab a fresh pair as seen below: SCR-20230901-ocf

Note: Just run zee5.sh(for linux/mac) or zee5.bat(windows) to execute everything at once. Update: the above method is for downloading shows, for downloading movies use zeemovie.py script.

Have any queries? PM me on telegram @swappyison

If you like my work and want to support me here's my kofi page----> https://ko-fi.com/swappyison
