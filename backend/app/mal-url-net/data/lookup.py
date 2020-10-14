import whois
import tldextract
import socket
import sys
import progressbar
import numpy as np
import pandas as pd
from pathlib import Path


def get_lookup_data(url, label):
    url_features = tldextract.extract(url)
    domain = url_features.domain+'.'+url_features.suffix
    try:
        whois_data = whois.whois(domain)
        domain_ip = int(socket.gethostbyname(domain).replace('.', ''))
        whois_server_features = tldextract.extract(whois_data["whois_server"])
        return [url, url_features.domain, url_features.suffix, whois_data["registrar"], whois_server_features.domain, whois_server_features.suffix, whois_data["org"], domain_ip, label]
    except:
        return None


def fetch_url_data():
    urls = np.array(pd.DataFrame(
        pd.read_csv((Path("data/") / "data.csv"), ',', error_bad_lines=False))
        .sample(frac=1).reset_index(drop=True))
    struct_data = pd.DataFrame(filter(None, [get_lookup_data(url[0], url[1]) for url in progressbar.progressbar(urls)]), columns=[
                               'url', 'url_domain', 'url_suffix', 'whois_registrar', 'whois_domain', 'whois_suffix', 'whois_org', 'url_domain_ip', 'label'])
    struct_data.to_csv(Path("data/") / "struct_data.csv",
                       encoding='utf-8', index=False)


fetch_url_data()
