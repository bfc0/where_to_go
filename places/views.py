from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Place
from .serializers import serialize_places


def all_places(request):
    places = Place.objects.prefetch_related("imgs")
    serialized_places = serialize_places(places)

    return render(request, "index.html", {"places": serialized_places})


def details(request, place_id):
    place: Place = get_object_or_404(
        Place.objects.prefetch_related("imgs"), id=place_id)

    serialized_place = {
        "title": place.title,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude,
        },
        "imgs": [img.image.url for img in place.imgs.all()],
    }

    return JsonResponse(serialized_place, json_dumps_params={"ensure_ascii": False})
