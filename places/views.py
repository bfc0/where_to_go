import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from .models import Place


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
                "coordinates": [place.coordinates.lng, place.coordinates.lat],
            },
            "properties": {
                "title": place.onmap_title,
                "placeId": place.onmap_title,
                "detailsUrl": "__placeholder",
            },
        }
        result["features"].append(feature)
    return result


def placeholder(request):
    places = Place.objects.all().prefetch_related("imgs")
    res = serialize_places(places)
    # print(res)
    serialized = json.dumps(res, ensure_ascii=False, cls=DjangoJSONEncoder, indent=4)
    return render(request, "index.html", {"places": serialized})


def details(request, id):
    place = get_object_or_404(Place, id=id)
    return HttpResponse(f"details for {place.title}")
