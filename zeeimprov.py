import json
from tqdm import tqdm
import requests
import subprocess
import re
import os
from urllib.parse import urlparse
from decouple import config

access_token = #place your value
auth_token = #place your value
x-dd-token = #place your value

# Read the URLs from show_urls.txt
with open("show_urls.txt", "r") as file:
    urls = file.readlines()

show_name = input('show_name:')
episode_number = 1
# Define the API endpoint URL
api_url = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

# Define common JSON data and headers
data = {
    'x-access-token': x-access-token,
    'Authorization': auth_token,
    'x-dd-token': x-dd-token
}



headers = {
    'User-Agent': 'YOUR_USER_AGENT',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Referer': 'https://www.zee5.com/',
    'Origin': 'https://www.zee5.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

output_directory = "subtitles"
os.makedirs(output_directory, exist_ok=True)

# Initialize episode number

# Initialize the progress bar
with tqdm(total=len(urls)) as pbar:
    # Loop through the URLs and make requests for each one
    for url in urls:
        # Remove leading/trailing whitespaces and newline characters
        url = url.strip()

        # Split the URL by '/' and get the relevant parts
        url_parts = url.split('/')

        # Extract the content_id and show_id from the URL
        content_id = url_parts[-1]  # Last part of the URL
        show_id = url_parts[-3]     # Second-to-last part of the URL
        print(f"Content ID: {content_id}, Show ID: {show_id}")

        # Define the payload data for this URL
        payload = {
        "content_id": content_id,
        "show_id": show_id,
        "device_id": "6c0d5e20-e7bb-41ad-8442-8519b0fada8a",
        "platform_name": "desktop_web",
        "translation": "en",
        "user_language": "en,hi,hr",
        "country": "IN",
        "state": "UT",
        "app_version": "3.13.0",
        "user_type": "register",
        "check_parental_control": "false",
        "gender": "Unknown",
        "uid": "75986e61-44dd-4b9e-bb91-d387028c6288",
        "ppid": "6c0d5e20-e7bb-41ad-8442-8519b0fada8a",
        "version": "12"
        }

        # Convert the JSON data dictionary to JSON format
        json_data = json.dumps(data)

        # Make the POST request with JSON data, payload, and headers for this URL
        response = requests.post(api_url, data=json_data, headers=headers, params=payload)

        # Check the response for this URL
        if response.status_code == 200:
            # Request was successful
            json_response = response.json()  # Parse JSON response
            subtitle_urls = json_response.get("assetDetails", {}).get("subtitle_url", [])

            # Iterate through subtitle URLs and extract the "url" field
            
            # Check if "keyOsDetails" is present in the JSON response
            if "keyOsDetails" in json_response:
                keyosdetails = json_response["keyOsDetails"]
                if "hls_token" in keyosdetails:
                    hls_token = keyosdetails["hls_token"]
                    print(f"hls_token: {hls_token}")

                    # Split the URL by slashes and extract relevant parts
                

                    # Construct the output filename
                    output_filename = f"{show_name}.Ep{episode_number}.mp4"
                    episode_number +=1
                    # Use subprocess to run yt-dlp command for each URL with the proper output filename
                    command = ['yt-dlp', '-o', output_filename, hls_token]
                    subprocess.run(command, check=True)

                    print(f"Downloaded: {output_filename}")
                    for subtitle_info in subtitle_urls:
                        subtitle_url = subtitle_info.get("url")
                        if subtitle_url:
                    # Extract the show name from the VTT URL
                    # Construct the output filename and path
                            output_filename = f"{show_name}_Ep{episode_number}.vtt"
                            output_path = os.path.join(output_directory, output_filename)

                    # Check if the file already exists
                    if not os.path.exists(output_path):
                        # Download the VTT file using yt-dlp with desired output filename and directory
                        subprocess.run(["yt-dlp", "--output", output_path, subtitle_url])
                        print(f"Downloaded: {output_filename}")
                    else:
                        print(f"Skipped: {output_filename} (Already downloaded)")

            else:
            # Request failed
                print(f"Request for URL '{url}' failed with status code {response.status_code}")

        # Update the progress bar
        pbar.update(1)
