import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from images_to_pdf import images_to_pdf

main_url = "https://www.readm.org"

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_chapters(id):
    """
    """
    get_url = main_url + '/manga/' + id
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    res = s.get(get_url)
    url_list = []
    if res.status_code == 200:
        soup = bs(res.text, 'lxml')
    links = soup.find_all('td', {'class': 'table-episodes-title'})
    for link in links:
        url = main_url + link.findChildren('a')[0].attrs.get('href')
        url_list.append(url)
    url_list.reverse()

    return url_list

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "lxml")
    urls = []
    img_url = ""
    for img in soup.find_all("img", {'class': 'img-responsive scroll-down'}):
        img_url = main_url + img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        img_url = urljoin(url, img_url)
       
        if is_valid(img_url) and img_url not in urls:
            urls.append(img_url)
    return urls

def download(urls, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    for url in urls:
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)
        # get the file name
        filename = os.path.join(pathname, url.split("/")[-1])
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)

        with open(filename, "wb") as f:
            f.write(response.content)
    images_to_pdf(pathname)

def main(id, name):
    # get all images
    print(f"Getting Chapters from the '{name}'")
    chapters = get_all_chapters(id)
    print(f"{len(chapters)} found in '{name}'")
    for chapter in tqdm(range(len(chapters))):
        imgs = get_all_images(chapters[chapter])
        # for each image, download it
        path = os.path.join(os.getcwd(), '..', 'Downloaded', name, chapters[chapter].split('/')[-2], "images")
        download(imgs, path)

if __name__ == "__main__":
    manga_id = input("Manga ID:")
    manga_name = input("Manga name:")
    main(manga_id, manga_name)