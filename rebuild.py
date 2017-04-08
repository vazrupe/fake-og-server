import re
from urllib.request import urlopen
from urllib.parse import urljoin

from bs4 import BeautifulSoup


open_graph_rgx = re.compile('^og:(?P<meta>.+)')

html_template = '''
<html>
  <head>
    {og_tags}
    <title>{title}</title>
    <meta http-equiv="refresh" content="0; {target_url}" />
  </head>
</html>
'''
open_graph_template = '<meta property="og:{metadata}" content="{content}" />'


def rebuild_page(source_url, target_url):
    source_open_graph_data = ogp_get(source_url)

    if source_open_graph_data is None:
        return None

    og_meta_tags = []
    for metadata, content in source_open_graph_data['og'].items():
        og_tag = open_graph_template.format(
            metadata=metadata,
            content=content
        )
        og_meta_tags.append(og_tag)

    og_tags_str = '\n    '.join(og_meta_tags)

    page_title = source_open_graph_data.get('page_title', '')
    return html_template.format(
        title=page_title,
        og_tags=og_tags_str,
        target_url=target_url
    )


def ogp_get(url, checked_url=None):
    result = {
        'og': {}
    }

    page_html = safe_get_url(url)
    if page_html is None:
        return None
    soup = BeautifulSoup(page_html, 'lxml')

    if soup.title:
        result['page_title'] = soup.title.string

    ogps = soup.find_all('meta', property=open_graph_rgx)
    for ogp in ogps:
        content = ogp.get('content')
        ogp_type = ogp.get('property')

        if content and ogp_type:
            match = open_graph_rgx.match(ogp_type)
            if match:
                meta = match.group('meta')

                result['og'][meta] = content

    frames = soup.find_all('frame')
    iframes = soup.find_all('iframe')

    checked_url = set([url]) if checked_url is None else checked_url
    in_pages = frames + iframes
    for in_page in in_pages:
        in_page_uri = in_page.get('src')

        if in_page_uri is None:
            continue

        in_page_url = urljoin(url, in_page_uri)

        if in_page_url in checked_url:
            continue
            
        checked_url.add(in_page_url)
        sub_result = ogp_get(in_page_url, checked_url)

        if sub_result:
            not_set_page_title = 'page_title' not in result
            if not_set_page_title and 'page_title' in sub_result:
                result['page_title'] = sub_result['page_title']

            update_og = {
                k: v
                for k, v in sub_result['og'].items()
                if k not in result['og'].keys()
            }
            result['og'].update(update_og)

    return result


def safe_get_url(url):
    try:
        url = urlopen(url)
        return url.read()
    except:
        pass
    return None


if __name__ == '__main__':
    rebuilding_page = rebuild_page('SOURCE_URL', 'TARGET_URL')
    print(rebuilding_page)
