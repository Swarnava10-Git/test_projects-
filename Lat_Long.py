import pandas as pd
from geopy.geocoders import Nominatim

def get_place_info(place):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(place)
    if location:
        return {
            'Place Name': location.address,
            'Latitude': location.latitude,
            'Longitude': location.longitude
        }
    else:
        return None

def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

# Read places from Excel file
file_path = 'p.xlsx'
df = pd.read_excel(file_path)
places = df['Place'].tolist()

place_info = []

for place in places:
    info = get_place_info(place)
    if info:
        place_info.append(info)

file_path = 'place_info.xlsx'
save_to_excel(place_info, file_path)
print(f"Place information saved to {file_path}")
