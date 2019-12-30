from bs4 import BeautifulSoup, NavigableString, Declaration, Comment
# import urllib3
import re
import requests
from error import logError
from support import getdict

def startscrap(url):
    # url = 'https://thatec-innovation.com/index.php'
    url = url.strip()
    try:
        res = requests.get(url)
    except:
        logError('Scraped Failed. ' + url )
        return 'Scrap Failed'
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    #Get All tags that has text attr.
    texts = soup.find_all(text=True)
    # text1 = soup.get_text()
    blacklist = [
        '[document]', 'link', 'noscript', 'header', 'html', 'meta',
        'head', 'input', 'script', 'footer', 
    ]
    title_flag = 0 # Page Title flag
    content = '' # content variable
    results = []  
    title = ''
    negative_words = getdict('negative.txt')
    for text in texts:
        if not text.strip() in negative_words:
            if text.parent.name not in blacklist: # Check if current element is in Blacklist
                if (text.parent.name == 'h1' or text.parent.name == 'h2') and title_flag == 0:
                    title = text
                    title_flag = 1
                    print(title)
                elif text.parent.name == 'p' or text.parent.name == 'div':
                    if text == '\n' or text == '\r' or text == '\r\n': # Check if the content is null
                        pass
                    elif isinstance(text, NavigableString): #Check if the element is Comment
                        if type(text) not in (Comment, Declaration): 
                            content += text
        # print(title)
    # print(content)
    results.append(title)
    results.append(content)
    return results
# rs = []
# rs = startscrap('https://www.desyncra.com/?post_type=product_page&p=2072')