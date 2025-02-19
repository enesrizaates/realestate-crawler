from django.db import models
from datetime import datetime


class Post(models.Model):
    cat1 = models.CharField(max_length=256, blank=True, null=True)
    cat2 = models.CharField(max_length=256, blank=True, null=True)
    cat3 = models.CharField(max_length=256, blank=True, null=True)
    cat4 = models.CharField(max_length=256, blank=True, null=True)
    cat0 = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    region = models.CharField(max_length=256, blank=True, null=True)
    district = models.CharField(max_length=256, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    m2_brut = models.CharField(max_length=256, blank=True, null=True)
    m2_net = models.CharField(max_length=256, blank=True, null=True)
    oda_sayisi = models.CharField(max_length=256, blank=True, null=True)
    bina_yasi = models.CharField(max_length=256, blank=True, null=True)
    bulundugu_kat = models.CharField(max_length=256, blank=True, null=True)
    kat_sayisi = models.CharField(max_length=256, blank=True, null=True)
    isitma = models.CharField(max_length=256, blank=True, null=True)
    banyo_sayisi = models.CharField(max_length=256, blank=True, null=True)
    balkon = models.CharField(max_length=256, blank=True, null=True)
    esyali = models.CharField(max_length=256, blank=True, null=True)
    kullanim_durumu = models.CharField(max_length=256, blank=True, null=True)
    site_icerisinde = models.CharField(max_length=256, blank=True, null=True)
    site_adi = models.CharField(max_length=256, blank=True, null=True)
    krediye_uygun = models.CharField(max_length=256, blank=True, null=True)
    kimden = models.CharField(max_length=256, blank=True, null=True)
    fiyat = models.CharField(max_length=256, blank=True, null=True)
    ilan_aks = models.CharField(max_length=256, blank=True, null=True)
    ilan_fiyat = models.CharField(max_length=256, blank=True, null=True)
    ilan_no = models.CharField(max_length=256, blank=True,
                               null=True, unique=True)
    ilan_Tarihi = models.CharField(max_length=256, blank=True, null=True)
    Emlak_Tipi = models.CharField(max_length=256, blank=True, null=True)
    area_brut = models.CharField(max_length=256, blank=True, null=True)
    area_net = models.CharField(max_length=256, blank=True, null=True)
    oda_sayisi = models.CharField(max_length=256, blank=True, null=True)
    bina_yasi = models.CharField(max_length=256, blank=True, null=True)
    floor = models.CharField(max_length=256, blank=True, null=True)
    total_floor = models.CharField(max_length=256, blank=True, null=True)
    isitma = models.CharField(max_length=256, blank=True, null=True)
    banyo_sayisi = models.CharField(max_length=256, blank=True, null=True)
    balkon = models.CharField(max_length=256, blank=True, null=True)
    esyali = models.CharField(max_length=256, blank=True, null=True)
    kullanim_durumu = models.CharField(max_length=256, blank=True, null=True)
    site_icerisinde = models.CharField(max_length=256, blank=True, null=True)
    aidat = models.CharField(max_length=256, blank=True, null=True)
    site_adi = models.CharField(max_length=256, blank=True, null=True)
    krediye_uygun = models.CharField(max_length=256, blank=True, null=True)
    kimden = models.CharField(max_length=256, blank=True, null=True)
    takas = models.CharField(max_length=256, blank=True, null=True)
    gecici_numara_servisi = models.CharField(max_length=256,
                                             blank=True,
                                             null=True
                                             )
    site_preference = models.CharField(max_length=256, blank=True, null=True)
    record_date_time = models.DateTimeField(default=datetime.now, blank=True)

def __str__(self):
    return self.name
