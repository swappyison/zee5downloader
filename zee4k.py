import requests
import json
import re
import base64
import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt
import subprocess
from pathlib import Path
import os
import urllib.parse
from decouple import config
import jwt

access_token = config('ACCESS_TOKEN')
auth_token = config('AUTH_TOKEN')
x-dd-token = config('X-DD-TOKEN')

decoded = jwt.decode(auth_token, options={"verify_signature": False})
deviceId = decoded['device_id']
uid = decoded['user_id']

# Define the function to process a single URL
def process_url(url):
    api_url = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

    # Define common JSON data and headers
    data = {
    'x-access-token': x-access-token,
    'Authorization': auth_token,
    'x-dd-token': x-dd-token
}    
    m3u8DL_RE = 'N_m3u8DL-RE'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
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
        'Cache-Control': 'no-cache',
    }

    # Loop through the URLs and make requests for each one
    # Remove leading/trailing whitespaces and newline characters
    url = url.strip()

    # Split the URL by '/' and get the relevant parts
    url_parts = url.split('/')

    # Extract the content_id and show_id from the URL
    content_id = url_parts[-1]  # Last part of the URL
    show_id = url_parts[-3]  # Second-to-last part of the URL

    # Define the payload data for this URL
    payload = {
        "content_id": content_id,
        "show_id": show_id,
        "device_id": deviceId,
        "platform_name": "desktop_web",
        "translation": "en",
        "user_language": "en,hi,hr",
        "country": "IN",
        "state": "UT",
        "app_version": "3.13.0",
        "user_type": "register",
        "check_parental_control": "false",
        "gender": "Unknown",
        "uid": uid,
        "ppid": deviceId,
        "version": "12"
    }

    # Convert the JSON data dictionary to JSON format
    json_data = json.dumps(data)

    # Make the POST request with JSON data, payload, and headers for this URL
    response = requests.post(api_url, data=json_data, headers=headers, params=payload)

    # Check the response for this URL
    if response.status_code == 200:
        # Request was successful
        try:
            # Parse the JSON response
            response_data = response.json()
            key_os_details = response_data.get("keyOsDetails", {})
            nl_data = key_os_details.get("nl")
            sdrm_data = key_os_details.get("sdrm")

            print(f"{nl_data}")
            print(f"{sdrm_data}")
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for URL '{url}'")

    # Split the URL by '/' and get the relevant parts
    url_parts = url.split('/')

    # Extract the content_id and show_id from the URL
    content_id = url_parts[-1]
    url = "https://gwapi.zee5.com/content/details/" + content_id + "?translation=en&country=IN&version=2"
    headers = {
        "x-access-token": access_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 (OK)

        data = response.json()  # Parse the JSON response

        # Check if the "video_details" field is present in the JSON data
        if "video_details" in data:
            video_details = data["video_details"]

            # Check if the "url" field is present in the video_details
            if "url" in video_details:
                url = video_details["url"]

                # Prepend the URL with the specified prefix
                mediacloudfront_url = "https://mediacloudfront.zee5.com" + url
                print("Media Cloudfront URL:", mediacloudfront_url)

                # Download the MPD manifest
                mpd_response = requests.get(mediacloudfront_url)
                mpd_response.raise_for_status()

                # Search for PSSH within <cenc:pssh> tags using regex
                pssh_matches = re.findall(r'<cenc:pssh>(.*?)</cenc:pssh>', mpd_response.text, re.DOTALL)

                if pssh_matches:
                    shortest_pssh = min(pssh_matches, key=len)
                    print("Shortest PSSH found in the MPD:")
                    print(shortest_pssh)
                else:
                    print("PSSH not found in the MPD.")
            else:
                print("The 'url' field is not present in the video_details.")
        else:
            print("The 'video_details' field is not present in the JSON response.")

    except requests.exceptions.RequestException as e:
        print("Error making the GET request:", e)

    except ValueError as e:
        print("Error parsing JSON response:", e)

    # Define your headers here
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/octet-stream',
        'Referer': 'https://www.zee5.com/',
        'nl': nl_data,
        'customdata': sdrm_data,
        'Origin': 'https://www.zee5.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    pssh = shortest_pssh
    lic_url = 'https://spapi.zee5.com/widevine/getLicense'

    def WV_Function(pssh, lic_url, cert_b64=None):
        wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)
        widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers)
        license_b64 = b64encode(widevine_license.content)
        wvdecrypt.update_license(license_b64)
        Correct, keyswvdecrypt = wvdecrypt.start_process()
        if Correct:
            return Correct, keyswvdecrypt

    correct, keys = WV_Function(pssh, lic_url)

    print()
    for key in keys:
        ke_ys = ' '.join([f'--key {key}' for key in keys]).split()
        print('--key ' + key)

        # Build the key_string to make all keys easily copyable
        key_string = ' '.join([f"--key {key}" for key in keys])

        # Use the pyperclip library to copy the key_string to the clipboard
        pyperclip.copy(key_string)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
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
            'Cache-Control': 'no-cache',
        }

        json_data = {
    'x-access-token': x-access-token,
    'Authorization': auth_token,
    'x-dd-token': x-dd-token
}        
        response = requests.post(
            api_url + "?content_id=" + content_id + "&show_id=" + show_id + "&device_id=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&platform_name=desktop_web&translation=en&user_language=en,hi,hr&country=IN&state=UP&app_version=3.14.4&user_type=register&check_parental_control=false&uid=75986e61-44dd-4b9e-bb91-d387028c6288&ppid=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&version=12",
            headers=headers,
            json=json_data,
        )

        # Parse the JSON response
        data = response.json()

        if 'assetDetails' in data:
            # Access the 'video_url' dictionary within 'assetDetails'
            video_url = data['assetDetails'].get('video_url', {})

            # Access the 'mpd' value within 'video_url'
            old_mpd_url = video_url.get('mpd', None)

            if old_mpd_url is not None:
                print("MPD Value:", old_mpd_url)

            else:
                print("'mpd' not found in 'video_url'")
        else:
            print("'assetDetails' not found in JSON response")

        # Define the replacement part
        pattern = r'/DDPLUS/([^/]+)/([^/]+)'
        
        matches = re.findall(pattern, old_mpd_url)

        # Extract the name from the matched groups
        if matches:
            combined_name = '_'.join(matches[0])
            print(combined_name)

        # Use re.findall to find all matching occurrences in the URL
        parsed_url = urllib.parse.urlparse(old_mpd_url)

# Get the file name from the path
        file_name = parsed_url.path.split("/")[-1]

# Modify the file name
        new_file_name = "manifest-connected-4k.mpd"

# Construct the new URL with the modified file name
        new_url = old_mpd_url.replace(file_name, new_file_name)
        subprocess.run([m3u8DL_RE,
                        '-M', 'format=mkv:muxer=ffmpeg',
                        '--concurrent-download',
                        '--log-level', 'INFO',
                        '--save-name', 'video',
                        new_url,  # Separate mpd_response.url from the previous options
                        *ke_ys
                        ])
        try:
            Path('video.mkv').rename('' + combined_name + '.mkv')
            print(f'{combined_name}.mkv \nall done!\n')
        except FileNotFoundError:
            print("[ERROR] no mkv file")
with open("show_urls.txt", "r") as file:
    urls = file.read().splitlines()

# Loop through the URLs and process each one
for url in urls:
    # Remove leading/trailing whitespaces and newline characters
    url = url.strip()
    # Call the function to process the URL
    process_url(url)
