from bs4 import BeautifulSoup
import urllib2
import re
# from app import CrawledLinks

def getLinks(url):
    url = url.strip()
    if url[-1] == '/':
        url = url[:-1]    
    try:
        html_page = urllib2.urlopen(url)
    except:
        return "unknown url"
    soup = BeautifulSoup(html_page)
    rst_links = []
    txt_dict=['about', 'assistant', 'blog', 'business', 'business plan', 'campus', 'careers', 'contact', 'contact cs', 'company', 'datasets',
        'equipment' , 'events', 'highlights', 'home', 'homepage', 'industries', 'inks', 'jobs', 'modules', 'news', 'news & events',             
        'partner', 'patients', 'product', 'principle', 'profile', 'profil', 'produkt', 'publications', 'send email', 'services', 'solutions', 'support', 
        'system', 'team', 'technology', 'training', 'university']
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    for link in soup.findAll('a'):
        txt = link.get_text()
        if txt.lower() in txt_dict:
            buf = []
            clink = link.get('href')
            clink = clink.strip()
            if url[-1] == '/':
                print('()()()()()()()()', url)
            if clink[0] == '.' or clink[0] == '#':
                clink = clink[1:]
            if clink[-1] != '/':
                clink == clink + '/'
            if clink is not None and regex.search(clink):
                urlbuf = clink
            else:
                if url[-1] == '/' and clink[0] == '/':
                    urlbuf = urlbuf = url + clink[1:]
                elif url[-3:] == clink[3:]:
                    urlbuf = url + clink[3:]
                elif url[-1] != '/' and clink[0] != '/':
                    urlbuf = url + '/' + clink
                else:
                    urlbuf = url + clink
                #     if url[-4:-1] == clink[0:3]:
                #         urlbuf = url + clink[3:]
                #     else:
                #         urlbuf = url + clink[1:]
                # else:
                #     if url[-4:-1] == clink[0:3]:
                #         urlbuf = url + clink[3:]
                #     else:
                #         urlbuf = url + clink
                print(urlbuf)
            buf.append(link.get_text())
            buf.append(urlbuf)
            rst_links.append(buf)
            # else:
            #     links.append(url + link.get('href'))
    rst_links = checkDuplicate(rst_links) 
    # rst_txts = checkDuplicate(txts)
    return rst_links
def checkDuplicate(inputList):
        results = [] 
        for item in inputList: 
            if item not in results: 
                results.append(item)
        return results 