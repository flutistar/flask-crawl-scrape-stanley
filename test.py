# from bs4 import BeautifulSoup, NavigableString, Declaration, Comment
# import urllib2
# import re
# import requests

# def startscrap(url):
#     # url = 'https://thatec-innovation.com/index.php'
#     try:
#         res = requests.get(url)
#     except:
#         return 'Scrap Failed'
#     html_page = res.content
#     soup = BeautifulSoup(html_page, 'html.parser')
#     #Get All tags that has text attr.
#     texts = soup.find_all(text=True)
#     # text1 = soup.get_text()
#     blacklist = [
#         '[document]', 'link', 'noscript', 'header', 'html', 'meta',
#         'head', 'input', 'script', 'footer', 
#     ]
#     allowlist = ['span', 'p', 'div', 'h3']
#     title_flag = 0 # Page Title flag
#     content = '' # content variable
#     results = []  
#     title = ''
#     txt_flag = 0
#     for text in texts:
#         # print(text.parent.name)
#         if text.parent.name not in blacklist: # Check if current element is in Blacklist
#             if (text.parent.name == 'h1' or text.parent.name == 'h2') and title_flag == 0:
#                 if text.strip() != '':
#                     title = text
#                     title_flag = 1
#                 print('ddddd', title)
#             elif text.parent.name in allowlist:
#                 if txt_flag == 0 and text.strip() != '':
#                     print(text)
#                     txt_flag = 1
#                 if text == '\n' or text == '\r' or text == '\r\n': # Check if the content is null
#                     pass
#                 elif isinstance(text, NavigableString): #Check if the element is Comment
#                     if type(text) not in (Comment, Declaration) and text.strip(): 
#                         content += text
#     # print(title)
#     # print(content)
#     results.append(title)
#     results.append(content)
#     return results
# rs = []
# rs = startscrap('https://www.ibmt.fraunhofer.de')
lists = ['aaa', 'aaac', 'caaa', 'qqq']
if not 'aaa ' in lists:
    print('insert')
else:
    print('Duplicated')