import requests
from urllib.parse import urlparse, parse_qs

# Input the base URL
base_url = input("Enter the base URL: ")

# Parse the input URL to extract query parameters
url_components = urlparse(base_url)
query_parameters = parse_qs(url_components.query)

# Extract the relevant query parameters
season_id = query_parameters.get("season_id", [""])[0]
episode_limit = int(query_parameters.get("limit", [25])[0])

# Define headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.zee5.com/',
    'x-access-token': input('access_token'),
    'Origin': 'https://www.zee5.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Connection': 'keep-alive',
}

total_episodes = 0
page = 0

# Create a list to store web URLs
web_urls = []

while True:
    # Create the URL for the current page
    page_url = f"{base_url}&page={page}"

    response = requests.get(page_url, headers=headers)

    if response.status_code == 200:
        print(f"Request for page {page} was successful.")
        data = response.json()  # Assuming the response is in JSON format

        # Check if 'episode' field exists in the response
        if 'episode' in data:
            episodes = data['episode']

            # Check if there are any episodes on this page
            if not episodes:
                break  # No more episodes, exit the loop

            # Iterate through episodes on this page
            for episode in episodes:
                if 'web_url' in episode:
                    web_url = episode['web_url']
                    total_episodes += 1

                    # Prepend the web URL with "https://www.zee5.com/"
                    web_url = f"https://www.zee5.com/{web_url}"

                    # Append the web URL to the list
                    web_urls.append(web_url)

                    print(f"Episode {total_episodes} Web URL: {web_url}")
        else:
            print("No 'episode' field found in the response.")
            break  # Exit the loop if there is an issue with the response structure
    else:
        print(f"Request for page {page} failed with status code {response.status_code}.")
        break  # Exit the loop if there is an error

    page += 1

print(f"Retrieved a total of {total_episodes} episodes.")

# Export the web URLs to a text file
with open('show_urls.txt', 'w') as file:
    for web_url in web_urls:
        file.write(f"{web_url}\n")

print("Web URLs exported to 'show_urls.txt' file.")
