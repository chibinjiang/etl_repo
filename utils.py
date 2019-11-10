from lxml import etree
from io import StringIO


def parse_html(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    text = '\n'.join([sent.text for sent in tree.iter() if sent.text is not None])
    return text


def replace_invalid_null_character(text):
    text = text.replace('\xa0', ' ')
    text = text.replace('\u3000', ' ')
    return text
