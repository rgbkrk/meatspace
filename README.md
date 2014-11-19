meatspace
=========

Track events bounded by time and space.

Goals:

* Stop using smarmy URLs like developer.avocado.com/php2014
* Track usage from an access point within a time range
* Register a new event with a simple registration page

```
pip install -r requirements.txt
python main.py
```

## API (in development)

```
curl 127.0.0.1:48879/api/events/
```

## Docker setup

Launching

```
docker run -p 48879:48879 rgbkrk/meatspace
```

Building (if you're developing locally)
```
docker build -t rgbkrk/meatspace .
```

