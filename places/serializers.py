import json
from django.core.serializers.json import DjangoJSONEncoder


def serialize_places(places):
    features = [
        {
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
        for place in places
    ]

    map_points = {
        "type": "FeatureCollection",
        "features": features,
    }

    return json.dumps(map_points, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4)
