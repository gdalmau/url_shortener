# URL Shortener
Webservice which shortens URLs like https://bitly.com/


# Installing the library

1. Clone the repository:
`git clone`

2. Create a virtual environment with Python 3.X (in the example Python 3.7):
```bash
sudo apt install virtualenvwrapper
mkvirtualenv url-shortener -p /usr/bin/python3.7
pip3 install .
```


# Running

Run the service with:

```bash
python3 url_shortener.py
```


# Running tests

Run the tests with:
```bash
python3 -m unittest tests/api_tests.py
```



# Endpoints

#### POST /shorten
The request body will have the following content:

```json
{
    "url": "https://www.google.com/",
    "shortcode": "google"
}
```

When no shortcode provided it should create a random shortcode for the
provided URL. The shortcode has a length of 6 characters and will contain only
alphanumeric characters or underscores.

Returns HTTP status 201 with the following body:

```json
{
    "shortcode": "google"
}
```

Errors:

| Code | Message                           |
|------|-----------------------------------|
| 400  | Url not present                   |
| 409  | Shortcode already in use          |
| 412  | The provided shortcode is invalid |


#### GET /<shortcode>
Returns HTTP status 302 with the Location header containing the URL

Errors:

| Code | Message             |
|------|---------------------|
| 404  | Shortcode not found |


#### GET /\<shortcode\>/stats
Returns HTTP status 200 with the following body:

```json
{
    "created": "2017-05-10T20:45:00.000Z",
    "lastRedirect": "2018-05-16T10:16:24.666Z",
    "redirectCount": 6
}
```

`<created>` contains the creation datetime of the shortcode (in ISO8601)
`<lastRedirect>` contains the datetime of the last usage of the shortcode (in
ISO8601)
`<redirectCount>` indicates the number of times the shortcode has been used

Errors:

| Code | Message             |
|------|---------------------|
| 404  | Shortcode not found |