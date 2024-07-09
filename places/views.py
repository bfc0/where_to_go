import html
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from .models import Place
from .serializers import serialize_places


def all_places(request):
    places = Place.objects.all().prefetch_related("imgs")
    serialized = serialize_places(places)

    return render(request, "index.html", {"places": serialized})


def details(request, id):
    place: Place = get_object_or_404(Place.objects.prefetch_related("imgs"), id=id)

    as_dict = {
        "title": place.title,
        "description_short": place.description_short,
        "description_long": mark_safe(html.unescape(place.description_long)),
        "coordinates": {
            "lng": place.coordinates.lng,
            "lat": place.coordinates.lat,
        },
        "imgs": [img.image.url for img in place.imgs.all()],
    }

    return JsonResponse(as_dict, json_dumps_params={"ensure_ascii": False})
