from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# API info
# Key
key = "1de0aca900a1f628f8e5806fd1984250"
# Secret Key
secret = "ad70a38bbaab5672"
wait_time = 1

# download folder
animalname = sys.argv[1]
savedir = "./" + animalname

flickrapi = FlickrAPI(key, secret, format='parsed-json')
result = flickrapi.photos.search(
    text=animalname,
    per_page=400,
    media='photos',
    sort='relevance',
    safe_search=1,
    extras='url_q, licence'
)

photos = result['photos']
# confirm
# pprint(photos)
for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    # overlap
    if os.path.exists(filepath):continue
    urlretrieve(url_q,filepath)
    time.sleep(wait_time)
