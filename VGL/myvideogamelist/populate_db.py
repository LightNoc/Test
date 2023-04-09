import requests
import os
import django
from django.db import transaction
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myvideogamelist.settings")
django.setup()

from catalog.models import Game, Platform, Genre

# Set up the IGDB API endpoint and parameters
url = "https://api.igdb.com/v4/games"
fields = "name, first_release_date, summary, genres.name, platforms.name, involved_companies.company.name"
order = "popularity:desc"
limit = 100
headers = {}
#Go here to get client_id and client_secret: https://dev.twitch.tv/console/apps/tl9nb7ec86byonfmy24qy0txfpkp0o
# Get the access token
auth_url = "https://id.twitch.tv/oauth2/token"
client_id = "tl9nb7ec86byonfmy24qy0txfpkp0o"
client_secret = "lwg8lgi7a5qefgsxyu4cri8x9x9s4j"
grant_type = "client_credentials"
response = requests.post(auth_url, params={"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type})

if response.status_code == 200:
    access_token = response.json()["access_token"]
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
    }

# Make the API request
response = requests.post(url, headers=headers, data=f"fields {fields}; sort {order}; limit {limit};")

# Parse the response and create objects for each game and platform
with transaction.atomic():
    for game_data in response.json():
        # Create the game object
        print(game_data.get("first_release_date"))
        first_release_date = game_data.get("first_release_date")
        if first_release_date:
            date = datetime.fromtimestamp(first_release_date).date()
        else:
            date = None
        game = Game(
            title=game_data["name"],
            release_date=date,
            summary=game_data.get("summary"),
            developer=game_data.get("involved_companies", [{}])[0].get("company", {}).get("name"),
            publisher=game_data.get("involved_companies", [{}])[0].get("company", {}).get("name"),
        )
        game.save()

        # Create the platform objects
        for platform_data in game_data.get("platforms", []):
            platform, created = Platform.objects.get_or_create(name=platform_data["name"])

            # Add the platform to the game's platforms
            game.platforms.add(platform)

        # Add the developer and publisher to the game object
        for company_data in game_data.get("involved_companies", []):
            company_name = company_data["company"]["name"]
            game.developer = company_name
            game.publisher = company_name

        # Create the genre objects
        for genre_data in game_data.get("genres", []):
            genre, created = Genre.objects.get_or_create(name=genre_data["name"])

            # Add the genre to the game's genres
            game.genres.add(genre)

transaction.commit()
