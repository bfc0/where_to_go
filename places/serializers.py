import json
from django.core.serializers.json import DjangoJSONEncoder


def serialize_places(places_list):
    result = {
        "type": "FeatureCollection",
        "features": [],
    }

    for place in places_list:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude],
            },
            "properties": {
                "title": place.title,
                "placeId": place.title,
                "detailsUrl": place.get_api_url(),
            },
        }
        result["features"].append(feature)
    return json.dumps(result, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4)
