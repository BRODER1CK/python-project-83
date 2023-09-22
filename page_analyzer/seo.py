from bs4 import BeautifulSoup


def get_seo(page):
    contents = BeautifulSoup(page, 'html.parser')
    title = contents.find('title').text if contents.find('title') else ''
    h1 = contents.find('h1').text if contents.find('h1') else ''
    description = contents.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']
    else:
        description = ''
    return title, h1, description
