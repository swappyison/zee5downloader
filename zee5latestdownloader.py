import requests
import re
import subprocess
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

m3u8DL_RE = 'N_m3u8DL-RE'
show_name = input("enter show name: ")
season_num = input("enter season number: ")
indexz = 1

def process_url(url):
    global indexz
    api_url = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

    # Define common JSON data and headers
    data = {
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTEwLTA0VDEwOjMwOjQ5LjAxNVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5NjQxNTQ0OX0.4_WfxDu8Caj1ZHyPdEzCUOGbdSYf3tAdB5RexA5y3z8",
        "Authorization": "bearer eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3NTk4NkU2MS00NERELTRCOUUtQkI5MS1EMzg3MDI4QzYyODgiLCJzdWJzY3JpcHRpb25zIjoiW3tcImlkXCI6XCJmNjc1MGM2Zi02MmI2LTExZWUtODBlZC02MWI4NjhiZGY0NGNcIixcInVzZXJfaWRcIjpcIjc1OTg2ZTYxLTQ0ZGQtNGI5ZS1iYjkxLWQzODcwMjhjNjI4OFwiLFwiaWRlbnRpZmllclwiOlwiQ1JNXCIsXCJzdWJzY3JpcHRpb25fcGxhblwiOntcImlkXCI6XCIwLTExLTIwNzNcIixcImFzc2V0X3R5cGVcIjoxMSxcInN1YnNjcmlwdGlvbl9wbGFuX3R5cGVcIjpcIlNWT0RcIixcInRpdGxlXCI6XCJQcmVwYWlkIENvZGUgUGFjayAtIDEyIG1vbnRoc1wiLFwib3JpZ2luYWxfdGl0bGVcIjpcIlByZXBhaWQgQ29kZSBQYWNrIC0gMTIgbW9udGhzXCIsXCJzeXN0ZW1cIjpcIlo1XCIsXCJkZXNjcmlwdGlvblwiOlwiUHJlbWl1bSAtIDEyIG1vbnRocyAtIHByZXBhaWQgY29kZXNcIixcImJpbGxpbmdfY3ljbGVfdHlwZVwiOlwiZGF5c1wiLFwiYmlsbGluZ19mcmVxdWVuY3lcIjozNjUsXCJwcmljZVwiOjY5OSxcImN1cnJlbmN5XCI6XCJJTlJcIixcImNvdW50cmllc1wiOltcIklOXCJdLFwic3RhcnRcIjpcIjIwMjItMDMtMTRUMTc6MDQ6MDBaXCIsXCJlbmRcIjpcIjIwMjQtMTItMzFUMjM6NTk6MDBaXCIsXCJvbmx5X2F2YWlsYWJsZV93aXRoX3Byb21vdGlvblwiOmZhbHNlLFwicmVjdXJyaW5nXCI6ZmFsc2UsXCJwYXltZW50X3Byb3ZpZGVyc1wiOlt7XCJuYW1lXCI6XCJaZWU1XCIsXCJwcm9kdWN0X3JlZmVyZW5jZVwiOm51bGx9XSxcInByb21vdGlvbnNcIjpbXSxcImFzc2V0X3R5cGVzXCI6WzAsNiw5XSxcImFzc2V0X2lkc1wiOltcIlwiXSxcImZyZWVfdHJpYWxcIjowLFwiYnVzaW5lc3NfdHlwZVwiOlwiZnJlZVwiLFwiYmlsbGluZ190eXBlXCI6XCJwcmVtaXVtXCIsXCJudW1iZXJfb2Zfc3VwcG9ydGVkX2RldmljZXNcIjoyLFwibW92aWVfYXVkaW9fbGFuZ3VhZ2VzXCI6W10sXCJ0dl9zaG93X2F1ZGlvX2xhbmd1YWdlc1wiOltdLFwiY2hhbm5lbF9hdWRpb19sYW5ndWFnZXNcIjpbXSxcImR1cmF0aW9uX3RleHRcIjpcIlwiLFwidmFsaWRfZm9yX2FsbF9jb3VudHJpZXNcIjp0cnVlLFwiYWxsb3dlZF9wbGF5YmFja19kdXJhdGlvblwiOjYsXCJvZmZlcl9pZFwiOjAsXCJjYXRlZ29yeVwiOlwiXCIsXCJhY3R1YWxfdmFsdWVcIjowLFwiYmVmb3JlVHZcIjp0cnVlfSxcInN1YnNjcmlwdGlvbl9zdGFydFwiOlwiMjAyMy0xMC0wNFQxMzowNzoyNS4wMDBaXCIsXCJzdWJzY3JpcHRpb25fZW5kXCI6XCIyMDI0LTEwLTAzVDIzOjU5OjU5WlwiLFwic3RhdGVcIjpcImFjdGl2YXRlZFwiLFwicmVjdXJyaW5nX2VuYWJsZWRcIjpmYWxzZSxcInBheW1lbnRfcHJvdmlkZXJcIjpudWxsLFwiZnJlZV90cmlhbFwiOm51bGwsXCJjcmVhdGVfZGF0ZVwiOm51bGwsXCJpcF9hZGRyZXNzXCI6bnVsbCxcImNvdW50cnlcIjpcIklOXCIsXCJhZGRpdGlvbmFsXCI6e1wicmVnaW9uXCI6XCJNQUhBUkFTSFRSQVwiLFwiY291bnRyeVwiOlwiSU5cIixcInBhcnRuZXJcIjpcIlpFRTVcIixcInN1YnNfdHlwZVwiOlwiaW50ZXJuYWxfc3Vic1wiLFwiY291cG9uY29kZVwiOlwiWjVDUEpBMjNZUk9RQjdcIixcImlwX2FkZHJlc3NcIjpcIjQ5LjM2LjIyMS40OSwgMjMuNTUuMjQ2LjcxLCAyMy41NS4yNDYuMjM4LDEwLjI0My43My4xNjJcIixcInBheW1lbnRtb2RlXCI6XCJQcmVwYWlkQ29kZVwifSxcImFsbG93ZWRfYmlsbGluZ19jeWNsZXNcIjowLFwidXNlZF9iaWxsaW5nX2N5Y2xlc1wiOjB9XSIsImFjdGl2YXRpb25fZGF0ZSI6IjIwMjEtMTItMDNUMDg6MDE6MDMuNDE3WiIsImFtciI6WyJkZWxlZ2F0aW9uIl0sImlzcyI6Imh0dHBzOi8vdXNlcmFwaS56ZWU1LmNvbSIsImN1cnJlbnRfY291bnRyeSI6IklOIiwiY2xpZW50X2lkIjoicmVmcmVzaF90b2tlbl9jbGllbnQiLCJhY2Nlc3NfdG9rZW5fdHlwZSI6IkRlZmF1bHRQcml2aWxlZ2UiLCJ1c2VyX3R5cGUiOiJSZWdpc3RlcmVkIiwic2NvcGUiOlsidXNlcmFwaSIsInN1YnNjcmlwdGlvbmFwaSIsInByb2ZpbGVhcGkiXSwiYXV0aF90aW1lIjoxNjkwNjA2NTA5LCJleHAiOjE2OTkwNTQ4NDcsImlhdCI6MTY5NjQyNDg0NywianRpIjoiMjdkZTliOWQtZGQyYi00MjZjLWJiZjYtNmU4ODRjYTFlMjI3IiwidXNlcl9lbWFpbCI6InN3YXBuaWx1cGFkaHlheWtyYXRvc0BnbWFpbC5jb20iLCJkZXZpY2VfaWQiOiI2YzBkNWUyMC1lN2JiLTQxYWQtODQ0Mi04NTE5YjBmYWRhOGEiLCJyZWdpc3RyYXRpb25fY291bnRyeSI6IklOIiwidmVyc2lvbiI6NSwiYXVkIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInN5c3RlbSI6Ilo1IiwibmJmIjoxNjk2NDI0ODQ3LCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiI3NTk4NmU2MS00NGRkLTRiOWUtYmI5MS1kMzg3MDI4YzYyODgiLCJjcmVhdGVkX2RhdGUiOiIyMDIxLTEyLTAzVDA4OjAxOjAzLjQxN1oiLCJhY3RpdmF0ZWQiOnRydWV9.itows8fWvFz-eReBEEklEoF08fvkg8oLBUzCtgtix9SRAf3Toql8LIZjIUEBDpFD1XIVM5L7_n_aWbEQgSKVHxyTITgV7KsTHL6qgdGegtXfHJzpb1tBU-xKARV3CXoO0JaZv7YNeFY4TUEr3RxeeH3PcBAKaKCxSt4QTjynBT8fjCC9oE7RCBxTZMrhxybgibXDGCtIUqy4xtJlNjXMrw-mtD21eD8yrGacgX_jfigvP1CCzPWuOMYnevRY66CMd7VVEt9q8TqK591k2veCZKJ7q4kXP9ojc3MhOMYlVEZz6_pWU1_eCeppe6uriDd60qZ77LBHHpPxbxjGrxmrmg",
        "x-dd-token": "eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ=="}
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
    url = url.strip()

    # Split the URL by '/' and get the relevant parts
    url_parts = url.split('/')

    content_id = url_parts[-1]  # Last part of the URL
    show_id = url_parts[-3]
    print(content_id)
    print(show_id)
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Referer': 'https://www.zee5.com/',
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

    json_data = {
        'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTEwLTI0VDEwOjMxOjU4LjQ2NVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5ODE0MzUxOH0.hKsRsKic5S9WENldti2HvuvZfDzHaZ7QXj6aTNH5GR0',
        'Authorization': 'bearer eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3NTk4NkU2MS00NERELTRCOUUtQkI5MS1EMzg3MDI4QzYyODgiLCJzdWJzY3JpcHRpb25zIjoiW3tcImlkXCI6XCJmNjc1MGM2Zi02MmI2LTExZWUtODBlZC02MWI4NjhiZGY0NGNcIixcInVzZXJfaWRcIjpcIjc1OTg2ZTYxLTQ0ZGQtNGI5ZS1iYjkxLWQzODcwMjhjNjI4OFwiLFwiaWRlbnRpZmllclwiOlwiQ1JNXCIsXCJzdWJzY3JpcHRpb25fcGxhblwiOntcImlkXCI6XCIwLTExLTIwNzNcIixcImFzc2V0X3R5cGVcIjoxMSxcInN1YnNjcmlwdGlvbl9wbGFuX3R5cGVcIjpcIlNWT0RcIixcInRpdGxlXCI6XCJQcmVwYWlkIENvZGUgUGFjayAtIDEyIG1vbnRoc1wiLFwib3JpZ2luYWxfdGl0bGVcIjpcIlByZXBhaWQgQ29kZSBQYWNrIC0gMTIgbW9udGhzXCIsXCJzeXN0ZW1cIjpcIlo1XCIsXCJkZXNjcmlwdGlvblwiOlwiUHJlbWl1bSAtIDEyIG1vbnRocyAtIHByZXBhaWQgY29kZXNcIixcImJpbGxpbmdfY3ljbGVfdHlwZVwiOlwiZGF5c1wiLFwiYmlsbGluZ19mcmVxdWVuY3lcIjozNjUsXCJwcmljZVwiOjY5OSxcImN1cnJlbmN5XCI6XCJJTlJcIixcImNvdW50cmllc1wiOltcIklOXCJdLFwic3RhcnRcIjpcIjIwMjItMDMtMTRUMTc6MDQ6MDBaXCIsXCJlbmRcIjpcIjIwMjQtMTItMzFUMjM6NTk6MDBaXCIsXCJvbmx5X2F2YWlsYWJsZV93aXRoX3Byb21vdGlvblwiOmZhbHNlLFwicmVjdXJyaW5nXCI6ZmFsc2UsXCJwYXltZW50X3Byb3ZpZGVyc1wiOlt7XCJuYW1lXCI6XCJaZWU1XCIsXCJwcm9kdWN0X3JlZmVyZW5jZVwiOm51bGx9XSxcInByb21vdGlvbnNcIjpbXSxcImFzc2V0X3R5cGVzXCI6WzAsNiw5XSxcImFzc2V0X2lkc1wiOltcIlwiXSxcImZyZWVfdHJpYWxcIjowLFwiYnVzaW5lc3NfdHlwZVwiOlwiZnJlZVwiLFwiYmlsbGluZ190eXBlXCI6XCJwcmVtaXVtXCIsXCJudW1iZXJfb2Zfc3VwcG9ydGVkX2RldmljZXNcIjoyLFwibW92aWVfYXVkaW9fbGFuZ3VhZ2VzXCI6W10sXCJ0dl9zaG93X2F1ZGlvX2xhbmd1YWdlc1wiOltdLFwiY2hhbm5lbF9hdWRpb19sYW5ndWFnZXNcIjpbXSxcImR1cmF0aW9uX3RleHRcIjpcIlwiLFwidmFsaWRfZm9yX2FsbF9jb3VudHJpZXNcIjp0cnVlLFwiYWxsb3dlZF9wbGF5YmFja19kdXJhdGlvblwiOjYsXCJvZmZlcl9pZFwiOjAsXCJjYXRlZ29yeVwiOlwiXCIsXCJhY3R1YWxfdmFsdWVcIjowLFwiYmVmb3JlVHZcIjp0cnVlfSxcInN1YnNjcmlwdGlvbl9zdGFydFwiOlwiMjAyMy0xMC0wNFQxMzowNzoyNS4wMDBaXCIsXCJzdWJzY3JpcHRpb25fZW5kXCI6XCIyMDI0LTEwLTAzVDIzOjU5OjU5WlwiLFwic3RhdGVcIjpcImFjdGl2YXRlZFwiLFwicmVjdXJyaW5nX2VuYWJsZWRcIjpmYWxzZSxcInBheW1lbnRfcHJvdmlkZXJcIjpudWxsLFwiZnJlZV90cmlhbFwiOm51bGwsXCJjcmVhdGVfZGF0ZVwiOm51bGwsXCJpcF9hZGRyZXNzXCI6bnVsbCxcImNvdW50cnlcIjpcIklOXCIsXCJhZGRpdGlvbmFsXCI6e1wicmVnaW9uXCI6XCJNQUhBUkFTSFRSQVwiLFwiY291bnRyeVwiOlwiSU5cIixcInBhcnRuZXJcIjpcIlpFRTVcIixcInN1YnNfdHlwZVwiOlwiaW50ZXJuYWxfc3Vic1wiLFwiY291cG9uY29kZVwiOlwiWjVDUEpBMjNZUk9RQjdcIixcImlwX2FkZHJlc3NcIjpcIjQ5LjM2LjIyMS40OSwgMjMuNTUuMjQ2LjcxLCAyMy41NS4yNDYuMjM4LDEwLjI0My43My4xNjJcIixcInBheW1lbnRtb2RlXCI6XCJQcmVwYWlkQ29kZVwifSxcImFsbG93ZWRfYmlsbGluZ19jeWNsZXNcIjowLFwidXNlZF9iaWxsaW5nX2N5Y2xlc1wiOjB9XSIsImFjdGl2YXRpb25fZGF0ZSI6IjIwMjEtMTItMDNUMDg6MDE6MDMuNDE3WiIsImFtciI6WyJkZWxlZ2F0aW9uIl0sImlzcyI6Imh0dHBzOi8vdXNlcmFwaS56ZWU1LmNvbSIsImN1cnJlbnRfY291bnRyeSI6IklOIiwiY2xpZW50X2lkIjoicmVmcmVzaF90b2tlbl9jbGllbnQiLCJhY2Nlc3NfdG9rZW5fdHlwZSI6IkRlZmF1bHRQcml2aWxlZ2UiLCJ1c2VyX3R5cGUiOiJSZWdpc3RlcmVkIiwic2NvcGUiOlsidXNlcmFwaSIsInN1YnNjcmlwdGlvbmFwaSIsInByb2ZpbGVhcGkiXSwiYXV0aF90aW1lIjoxNjkwNjA2NTA5LCJleHAiOjE2OTkwNTQ4NDcsImlhdCI6MTY5NjQyNDg0NywianRpIjoiMjdkZTliOWQtZGQyYi00MjZjLWJiZjYtNmU4ODRjYTFlMjI3IiwidXNlcl9lbWFpbCI6InN3YXBuaWx1cGFkaHlheWtyYXRvc0BnbWFpbC5jb20iLCJkZXZpY2VfaWQiOiI2YzBkNWUyMC1lN2JiLTQxYWQtODQ0Mi04NTE5YjBmYWRhOGEiLCJyZWdpc3RyYXRpb25fY291bnRyeSI6IklOIiwidmVyc2lvbiI6NSwiYXVkIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInN5c3RlbSI6Ilo1IiwibmJmIjoxNjk2NDI0ODQ3LCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiI3NTk4NmU2MS00NGRkLTRiOWUtYmI5MS1kMzg3MDI4YzYyODgiLCJjcmVhdGVkX2RhdGUiOiIyMDIxLTEyLTAzVDA4OjAxOjAzLjQxN1oiLCJhY3RpdmF0ZWQiOnRydWV9.itows8fWvFz-eReBEEklEoF08fvkg8oLBUzCtgtix9SRAf3Toql8LIZjIUEBDpFD1XIVM5L7_n_aWbEQgSKVHxyTITgV7KsTHL6qgdGegtXfHJzpb1tBU-xKARV3CXoO0JaZv7YNeFY4TUEr3RxeeH3PcBAKaKCxSt4QTjynBT8fjCC9oE7RCBxTZMrhxybgibXDGCtIUqy4xtJlNjXMrw-mtD21eD8yrGacgX_jfigvP1CCzPWuOMYnevRY66CMd7VVEt9q8TqK591k2veCZKJ7q4kXP9ojc3MhOMYlVEZz6_pWU1_eCeppe6uriDd60qZ77LBHHpPxbxjGrxmrmg',
        'x-dd-token': 'eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ==',
    }

    response = requests.post(
        'https://spapi.zee5.com/singlePlayback/getDetails/secure?content_id=' + content_id + '&show_id=' + show_id + '&device_id=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&platform_name=desktop_web&translation=en&user_language=en,hi,hr&country=IN&state=DL&app_version=3.15.5&user_type=premium&check_parental_control=false&uid=75986e61-44dd-4b9e-bb91-d387028c6288&ppid=6c0d5e20-e7bb-41ad-8442-8519b0fada8a&version=12',
        headers=headers,
        json=json_data,
    )

    data = response.json()
    content_url = data["assetDetails"]["video_url"]["mpd"]
    print(content_url)
    curl_command = f'''curl -s -X GET "{content_url}" \
                                                                    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36" \
                                                                     \
                                                                    --referer "https://www.zee5.com/" \
                                                                    | grep -o '<cenc:pssh>.*</cenc:pssh>' | sed 's/<cenc:pssh>//;s/<\/cenc:pssh>//' '''
    try:
        output = subprocess.check_output(curl_command, shell=True, text=True)
        print("Curl command executed successfully.")

        # Use regular expressions to extract base64-encoded data
        base64_encoded_data = re.findall(r'[A-Za-z0-9+/]+={0,2}', output)
        shortest_pssh = min(base64_encoded_data, key=len)
        # Get the first unique base64-encoded string
        unique_data = next(iter(set(base64_encoded_data)), None)
        pssh = shortest_pssh
        print(pssh)
    except:
        print()
    lic_url = 'https://spapi.zee5.com/widevine/getLicense'
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


        subprocess.run([m3u8DL_RE,
                '-M', 'format=mkv:muxer=ffmpeg',
                '--concurrent-download',
                '--log-level', 'INFO',
                '--save-name', 'video',
                content_url,  # Separate mpd_response.url from the previous options
                *ke_ys
                ])
        title = f'{show_name} - S{season_num} - E{indexz}'

        try:
            Path('video.mkv').rename('' + title + '.mkv')
            print(f'{title}.mkv \nall done!\n')
            indexz += 1
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
