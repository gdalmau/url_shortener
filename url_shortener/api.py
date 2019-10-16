from flask import request, make_response, jsonify
from flask_restful import Resource
from url_shortener.models import URLShortenModel, URLShortenSchema
from url_shortener.config import db, SHORTCODE_LENGHT
from url_shortener.utils import validate_shortcode, generate_shortcode
from datetime import datetime

RESPONSE_MESSAGES = {
    400: 'Url not present',
    404: 'Shortcode not found',
    409: 'Shortcode already in use',
    412: 'The provided shortcode is invalid',
}


def get_shortened_url(shortcode):
    return URLShortenModel.query.filter_by(
        shortcode=shortcode
    ).one_or_none()


def shortcode_exists(shortcode):
    return not get_shortened_url(shortcode)


def generate_unique_shortcode(length):
    shortcode = generate_shortcode(length)
    if shortcode_exists(shortcode):
        return generate_unique_shortcode(length)
    return shortcode


def custom_response(status_code, body=None, headers=None):
    if body is None:
        body = {
            'message': RESPONSE_MESSAGES.get(status_code)
        }
    json_body = jsonify(body) if isinstance(body, dict) else body
    return make_response(json_body, status_code, headers)


def create_shortened_url(url, shortcode):
    schema = URLShortenSchema()
    url_shorten = schema.load(
        {'url': url, 'shortcode': shortcode}, session=db.session
    )
    db.session.add(url_shorten)
    db.session.commit()
    return custom_response(201, body=dict(shortcode=shortcode))


class URLShorten(Resource):
    @staticmethod
    def post():
        json_data = request.get_json()
        if 'url' not in json_data:
            return custom_response(400)
        shortcode = json_data.get('shortcode')
        if shortcode:
            if not validate_shortcode(shortcode):
                return custom_response(412)
            existing_url = get_shortened_url(shortcode)
            if existing_url:
                return custom_response(409)
        else:
            shortcode = generate_unique_shortcode(length=SHORTCODE_LENGHT)

        return create_shortened_url(json_data['url'], shortcode)


class Shortcode(Resource):
    @staticmethod
    def get(shortcode):
        url = get_shortened_url(shortcode)
        if not url:
            return custom_response(404)
        else:
            url.last_redirect = datetime.now()
            url.redirect_count += 1
            db.session.commit()
            return custom_response(302, body='', headers={'Location': url.url})


class ShortcodeStats(Resource):
    @staticmethod
    def get(shortcode):
        url = get_shortened_url(shortcode)
        if not url:
            return custom_response(404)
        else:
            last_redirect = url.last_redirect and url.last_redirect.isoformat()
            body = {
                'created': url.created_at.isoformat(),
                'lastRedirect': last_redirect,
                'redirectCount': url.redirect_count,
            }
            return custom_response(200, body=body)


RESOURCES = [
    (URLShorten, '/shorten'),
    (Shortcode, '/<shortcode>'),
    (ShortcodeStats, '/<shortcode>/stats'),
]
