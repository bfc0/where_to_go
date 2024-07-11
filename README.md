# Places to Visit

A simple backend for a where to go website

[App demo](https://bfc0.pythonanywhere.com/)

## Install:
```bash
git clone https://github.com/bfc0/where_to_go.git
cd where_to_go
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "your_super_secret_django_key" >.env
python manage.py migrate
```

### If you are running the server with debug=False
```bash
python manage.py collectstatic
```

## Run the server
```bash
python manage.py runserver
```
## Populate Data:
[Data](https://github.com/devmanorg/where-to-go-places/tree/master)
```bash
git clone https://github.com/devmanorg/where-to-go-places.git somewhere
python manage.py importdir somewhere/places/
```

you can also import data from a single json file:
```bash
python manage.py importplace placename.json
```

### json format:
```json
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```


