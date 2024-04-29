from secrets import client_id

from database import SessionLocal
from models import Anime, Tag
from tqdm import tqdm
import requests

url = "https://api.myanimelist.net/v2/anime"

headers = {
    "X-MAL-CLIENT-ID": client_id,
}

db = SessionLocal()

for i in tqdm(range(1000)):
    response = requests.get(
        url+f"/{i}?fields=id,title,rank,genres,synopsis",
        headers=headers,
        timeout=2
    )
    if response.status_code != 200:
        continue

    response = response.json()

    new_anime = Anime(
        title=response['title'],
        description=response['synopsis'],
        rating=response['rank'],
    )

    for tag in response['genres']:
        tag_name = tag['name']
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        new_anime.tags.append(tag)
        db.add(new_anime)
        db.commit()

db.close()
