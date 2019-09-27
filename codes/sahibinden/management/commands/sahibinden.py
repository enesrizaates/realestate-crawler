from django.core.management.base import BaseCommand, CommandError

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
from utils import cookies
import shutil
import csv

def url_generator(url):
    response = requests.get(
        url, headers=cookies.headers, cookies=cookies.cookies
    )

    html = response.text
    soup = bs(html, 'lxml')
    links = []
    for link in soup.find_all('a'):
        val = link.get('href')
        if val and val.startswith('/ilan/'):
            links.append(val)
    ann_urls = []
    for link in links:
        ann_url = 'https://www.sahibinden.com' + link
        ann_urls.append(ann_url)
    return ann_urls

def soup_generator(ann_url):
    response = requests.get(
    ann_url, headers=cookies.headers,
    cookies=cookies.cookies
                            )
    html = response.text
    soup = bs(html, 'lxml')
    return soup

def main(soup):
    ann_main = soup.find_all(
        'script', attrs={'id': 'gaPageViewTrackingData'}
    )

    main_text = ann_main[0].text
    main_text = main_text.replace(
        'var pageTrackData = ', ''
    ).replace('\n', '').replace(';', '')

    main_json = json.loads(main_text)
    df_main = pd.DataFrame()
    vals = dict()
    for data in main_json['dmpData']:
        try:
            if data.get('name') and data.get('value'):
                vals[data['name']] = data['value']
        except Exception:
            pass

    for data in main_json['customVars']:
        try:
            if data.get('name') and data.get('value'):
                vals[data['name']] = data['value']
        except Exception:
            pass
    df_main = pd.DataFrame(vals, index=[0])
    return df_main

def get_descriptions(soup):
    descriptions = soup.find_all(
        'div', attrs = {'id':'classifiedDescription'}
    )
    df_descriptions = pd.DataFrame(descriptions, index=[0])
    print(df_descriptions)
    return df_descriptions



def get_properties(soup):
    properties = soup.find_all(
'li', attrs = {'class':'selected'}
)
    properties_val = []
    properties_val = ', '.join(
[item.text.replace('\n','').strip() for item in properties]
)
    return properties_val


def get_img_url(soup):
    images = soup.find_all('img')
    ls_images = []
    for image in images:
        try:
            img = image.get('data-src')
            if '.jpg' and 'x5' in img:
                ls_images.append(img)
        except Exception:
            pass
    return ls_images


def download_image(url, directory='./pictures'):
    response = requests.get(url,
                    cookies=cookies.cookies,
                    headers=cookies.headers,
                    stream=True
                    )
    image_name = url.split('/')[-1]
    image_path = '{}/{}'.format(directory, image_name)

    with open(image_path, 'wb') as out_file:
        # response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
    del response

    return image_path


class Command(BaseCommand):
    help = 'Closes the specified poll for voiting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        main_url = 'https://www.sahibinden.com/satilik'
        ann_urls = url_generator(main_url)

        for i in ann_urls:
            soup = soup_generator(i)
            df_main = main(soup)
            df_descriptions = get_descriptions(soup)
            properties_val = get_properties(soup)
            ls_images = get_img_url(soup)
            for url in ls_images:
                download_image(url)
            break

        directory = './pictures'

        with open('urls.csv', 'w', newline='') as urls:
            wr = csv.writer(urls, quoting=csv.QUOTE_ALL)
            wr.writerow(ls_images)

        df_main.to_csv('main.csv')
        df_descriptions.to_csv('desc.csv')

        from sahibinden.models import Post
        for index, row in df_main.iterrows():
            post = Post()
            post.cat1 = row['cat1']
            post.cat2 = row['cat2']
            post.cat3 = row['cat3']
            post.cat4 = row['cat4']
            post.cat0 = row['cat0']
            post.country = row['loc1']
            post.city = row['loc2']
            post.region = row['loc3']
            post.district = row['loc4']
            post.street = row['loc5']
            post.m2_brut = row['m2_brut']
            post.m2_net = row['m2_net']
            post.oda_sayisi = row['oda_sayisi']
            post.bina_yasi = row['bina_yasi']
            post.bulundugu_kat = row['bulundugu_kat']
            post.kat_sayisi = row['kat_sayisi']
            post.isitma = row['isitma']
            post.banyo_sayisi = row['banyo_sayisi']
            post.balkon = row['balkon']
            post.esyali = row['esyali']
            post.kullanim_durumu = row['kullanim_durumu']
            post.site_icerisinde = row['site_icerisinde']
            post.site_adi = row['site_adi']
            post.krediye_uygun = row['krediye_uygun']
            post.kimden = row['kimden']
            post.fiyat = row['fiyat']
            post.ilan_aks = row['ilan_aks']
            post.ilan_fiyat = row['ilan_fiyat']
            post.ilan_no = row['İlan No']
            post.ilan_Tarihi = row['İlan Tarihi']
            post.Emlak_Tipi = row['Emlak Tipi']
            post.area_brut = row['m² (Brüt)']
            post.area_net = row['m² (Net)']
            post.oda_sayisi = row['Oda Sayısı']
            post.bina_yasi = row['Bina Yaşı']
            post.floor = row['Bulunduğu Kat']
            post.total_floor = row['Kat Sayısı']
            post.isitma = row['Isıtma']
            post.banyo_sayisi = row['Banyo Sayısı']
            post.balkon = row['Balkon']
            post.esyali = row['Eşyalı']
            post.kullanim_durumu = row['Kullanım Durumu']
            post.site_icerisinde = row['Site İçerisinde']
            post.aidat = row['Aidat (TL)']
            post.site_adi = row['Site Adı']
            post.krediye_uygun = row['Krediye Uygun']
            post.kimden = row['Kimden']
            post.takas = row['Takas']
            post.gecici_numara_servisi = row['Geçici Numara Servisi']
            post.site_preference = row['site_preference']
        post.save()
