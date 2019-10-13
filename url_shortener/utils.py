import re, string, random
from config import SHORTCODE_LENGHT


def validate_shortcode(shortcode, length=False):
    shortcode_len = length or SHORTCODE_LENGHT
    return (
        len(shortcode) == shortcode_len and
        bool(re.match(r'^\w+$', shortcode))
    )


def generate_shortcode(length):
    valid_characters = (string.ascii_letters + string.digits + '_')
    return ''.join(random.choice(valid_characters) for _ in range(length))
