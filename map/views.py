from django.shortcuts import render
import os
import json
import requests
import pandas as pd
from .models import pharmacy
from geopy.distance import geodesic

# Create your views here.
def index(request):
    lat_lang = get_user_location_by_ip()

    recommended_pharmacies = []

    if pharmacy.objects.all().count() == 0:
        pharmacy_data = pd.read_csv("api/data/pharmacy.csv", encoding='utf-8')
        for _, row in pharmacy_data.iterrows():
            insert_map = pharmacy(name=row['약국명'], address=row['주소'], lat=row['병원경도'], lng=row['병원위도'])
            insert_map.save()

    for p in pharmacy.objects.all():
        # 위도와 경도 열 이름 확인

        pharmacy_location = (p.lng, p.lat)
        distance = geodesic(lat_lang, pharmacy_location).km

        if distance <= 1:
            recommended_pharmacies.append({
                'name': p.name,
                "address": p.address,
                'lat': p.lat,
                'lng': p.lng,
                "distance": round(distance, 2),
            })

    return render(request, 'map/index.html',{'pharmacies':recommended_pharmacies})


# Create your models here.
def get_user_location_by_ip():
    try:
        google_api_key = os.environ.get('GOOGLE_API_KEY')
        url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={google_api_key}'

        response = json.loads(requests.post(url).text)

        location = response['location']
        lat = location['lat']
        lng = location['lng']
        lat_lng = (lat, lng)
        return lat_lng
    except Exception as e:
        print("IP 기반 위치를 가져오는 데 실패했습니다.", str(e))
        return None
