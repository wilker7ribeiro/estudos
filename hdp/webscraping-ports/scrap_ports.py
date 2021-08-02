import sys
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
index_href = "https://docs.cloudera.com/HDPDocuments/HDP3/HDP-3.1.0/administration/content/configuring-ports.html"
index_html = requests.get(index_href).content

index_soup = BeautifulSoup(index_html, 'html.parser')
links_el = index_soup.select('.ullinks li a')
def if_is_string(value):
    return value if type(value) == str else ''

def process_component_from_link(link):
    port_link_href = urljoin(index_href, link)
    port_link_html = requests.get(port_link_href).content
    port_link_soup = BeautifulSoup(port_link_html, 'html.parser')

    port_title = port_link_soup.select_one('.title.topictitle1')
    len(port_title.text.split(' '))
    component = ' '.join(port_title.text.split(' ')[0:-(len(port_title.text.split(' ')) - 1)])
    def get_item_table_description(item):
        string = '# '+item[0].strip()
        if len(item) <= 6:
            return string
        if not item[4] or not type(item[4]) == str:
            return string
        string += ' - '+re.sub(r'\s+', ' ', item[4])
        if not item[6] or not type(item[6]) == str:
            return string
        return string + ' - '+re.sub(r'\s+', ' ', item[6])

    if rows := port_link_soup.select('.table tbody tr.row'):
        items = [ [ td.text.strip() for td in row.select('td') ] for row in rows ]
        items = list(filter(lambda item: re.match(r'([\d,\s/-]+)', item[2]), items))
        return '## '+component+'\n' + '\n'.join([
            get_item_table_description(item) + "\n" 
                +'\n'.join(['EXPOSE '+ port.strip() for port in re.split(',|/', re.sub(r'([\d,\s/-]+).*',r'\1', item[2]))])
            for item in items
        ])
    elif sections := port_link_soup.select('#content section'):
        regex = r'(.*)\((.*)\)'
        return '## '+component+'\n' + '\n'.join([
            f"# {section.find('h2').text} - { match[1] }\nEXPOSE {port.strip().replace('–', '-')}"
            for section in sections
            for item in section.find_all('li') if (match := re.search(regex, item.text.strip()).groups())
            for port in match[0].split(',') 
        ])

sys.stdout.write('\n\n'.join([process_component_from_link(a.attrs['href']) for a in links_el])+'\n')

