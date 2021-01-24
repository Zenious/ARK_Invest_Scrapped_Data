import requests
import csv
import hashlib
import os

url ={
    "arkf": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv",
    "arkq": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
    "arkk": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
    "arkw": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "arkg": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
    "prnt": "https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv",
    "izrl": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv",
} 


def getEtfMd5(ticker):
    latest_file = "./{}/latest.csv".format(ticker)
    latest_file_md5 = hashlib.md5()
    if not os.path.exists(ticker):
        os.makedirs(ticker)
        return "DONT_EXIST"
    with open(latest_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            latest_file_md5.update(chunk)
    return latest_file_md5.hexdigest()


def __init__():
    for etf_ticker, etf_url in url.items():
        with requests.Session() as s:
            download = s.get(etf_url)
            decoded_content = download.content.decode('utf-8')
            curr_file_md5 = hashlib.md5(download.content).hexdigest()
            latest_file_md5 = getEtfMd5(etf_ticker)
            if curr_file_md5 == latest_file_md5: # Same as previous file
                print("[X] No update to latest {} holdings details".format(etf_ticker))
                continue
            cr = csv.DictReader(decoded_content.splitlines(), delimiter=',',)
            my_list = list(cr)
            date = my_list[0]['date']
            with open("./{}/{}.csv".format(etf_ticker, date.replace("/", "_")), "w") as f:
                f.write(decoded_content)
            with open("./{}/latest.csv".format(etf_ticker), "w") as f:
                f.write(decoded_content)     
            print("[V] Updated latest {} holdings details".format(etf_ticker))  
    