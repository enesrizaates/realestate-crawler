from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
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
    ann_urls = list(dict.fromkeys(ann_urls))
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
    return vals

def get_descriptions(soup):
    descriptions = soup.find_all(
        'div', attrs = {'id':'classifiedDescription'}
    )
    df_descriptions = pd.DataFrame(descriptions, index=[0])
    return df_descriptions



def get_properties(soup):
    properties = soup.find_all(
'div', attrs = {'id':'classifiedProperties'}
)

    properties_list = []
    for item in properties:
        properties_val=item.text
    for element in properties_val.split('\n'):
        if element != '':
            properties_list.append(element.strip())
    properties_all = []
    properties_selected = []
    for i in soup.find_all('li',attrs={'class':'selected'}):
        properties_selected.append(i.text.replace('\n','').strip())
    for k in properties[0].find_all('li'):
        properties_all.append(k.text.replace('\n','').strip())
    properties_all.append('ilan_no')
    main_json = json.loads(soup.find_all('script',
                                         attrs={'id':'gaPageViewTrackingData'})[0].text.replace('var pageTrackData = ','').replace('\n','').replace(';',''))
                           
    ilan_no=[s['value'] for s in main_json['customVars'] if s['name']=='İlan No']
    values_all=[]
    properties_all = list(set(properties_all))
    properties_selected = list(set(properties_selected))
    properties_all.sort()
    properties_selected.sort()
    lookup = [x for x,y in enumerate(properties_all) if y in properties_selected]
    list1 = [properties_all[i] for i in lookup]
    l1 = [False for i in properties_all]
    for i in lookup:
        l1[i] = True
    zipped = zip(properties_all, l1)
    df = pd.DataFrame(zipped)
    df = df.transpose()
    df.columns = df.loc[0]
    df = df.drop(0)
    df['ilan_no'] = ilan_no
    return df


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
        df_main = pd.DataFrame()
        ls_main = []
        x = 0
        for i in ann_urls:
            soup = soup_generator(i)
            ls_main.append(main(soup))
            df_descriptions = get_descriptions(soup)
            properties_val = get_properties(soup)
            properties_val.to_csv('properties.csv')
            ls_images = get_img_url(soup)
            import pdb
            pdb.set_trace()
            for url in ls_images:
                download_image(url)
            x += 1
            if x >= 3:
                break
        df_main = pd.DataFrame(ls_main)
        directory = './pictures'

        with open('urls.csv', 'w', newline='') as urls:
            wr = csv.writer(urls, quoting=csv.QUOTE_ALL)
            wr.writerow(ls_images)

        df_main.to_csv('main.csv')
        df_descriptions.to_csv('desc.csv')
        from sahibinden.models import Post
        for index, row in df_main.iterrows():
            post = Post.objects.filter(ilan_no=row['İlan No']).first()
            if not post:
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
