from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import progressbar
from pathlib import Path
import re
import logging

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_all_available_link_urls(url):
  try:
    if re.match(regex, url) is None:
      url = "https://" + url
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    return [link['href'] for link in soup.find_all('a')]
  except Exception as e:
    logging.error(e)

def fetch_url_data():
  urls = np.array(pd.DataFrame(pd.read_csv((Path("./") / "data.csv"), ',', error_bad_lines=False)).sample(frac=1).reset_index(drop=True))
  struct_data = pd.DataFrame([(get_all_available_link_urls(url[0]), url[1]) for url in progressbar.progressbar(urls)])
  struct_data.to_csv(Path("./") / "link_data.csv", encoding='utf-8', index=False)

fetch_url_data()

