import re

def is_cyr_or_dig(string):
    pattern = r'^[\u0400-\u04FF\d]+$'
    return bool(re.match(pattern, string))