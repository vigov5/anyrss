import requests
from datetime import datetime
import pytz
from lxml import etree
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import urllib3

urllib3.disable_warnings()

def fetch_and_parse(url):
    try:
        html = requests.get(url, verify=False)
        soup = BeautifulSoup(html.text, "html.parser")
        root =  etree.HTML(str(soup))
        tree = etree.ElementTree(root)

        return root, tree, None
    except Exception as e:
        return None, None, str(e)


def gen_feed(name, url, date_format, items):
    fg = FeedGenerator()
    fg.load_extension('dc')
    fg.title(name)
    fg.description(name)
    fg.link(href=url, rel='alternate')

    # Add items to the feed
    for item_data in items:
        fe = fg.add_entry()
        fe.guid(item_data['guid'])
        fe.title(item_data['title'])
        fe.description(item_data['description'])
        fe.link(href=item_data['link'])
        date_obj = datetime.strptime(item_data['date'], date_format)
        date_utc = date_obj.astimezone(pytz.UTC)
        fe.published(date_utc)
        if 'tag' in item_data:
            fe.category(category={'label': item_data['tag'], 'term': item_data['tag'], 'scheme': ''})

    # Generate the RSS feed
    return fg.rss_str(pretty=True)


def extract_data_from(root, config):
    try:
        results = []
        if 'base' not in config:
            return None, f'No base config found!'
        
        base_elements = root.xpath(config['base'])
        
        if 'date_format' not in config:
            return None, f'No "date_format" config found!'

        for base_element in base_elements:
            one_result = {}
            for key in ['guid', 'title', 'description', 'link', 'date', 'tag']:
                if key in config:
                    if base_element.xpath(config[key]):
                        first_element = base_element.xpath(config[key])[0]
                        if type(first_element) is not etree._ElementUnicodeResult:
                            first_element = first_element.text

                        one_result[key] = first_element.strip()
                        if key == 'link' and not first_element.startswith('http'):
                            if 'link_prefix' in config:
                                one_result[key] = config['link_prefix'] + one_result[key]
                            else:
                                return None, f'Relative link but no "link_prefix" defined!'
                elif key != 'tag':
                    return None, f'Required key "{key}" is missing!'
            if one_result:
                results.append(one_result)
        
        return results, None
    except Exception as e:
        return None, str(e)