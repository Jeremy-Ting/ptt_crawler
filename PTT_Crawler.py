import requests, scrapy
from requests_html import HTML

widths = [
        (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
        (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
        (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
        (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
        (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
        (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
        (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
        (120831, 1), (262141, 2), (1114109, 1),
]

def calc_len(string):
    def chr_width(o):
        global widths
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1
    return sum(chr_width(ord(c)) for c in string)

def pretty_print(push, title, date, author):
    pattern = '%3s\t%s%s%s\t%s'
    padding = ' ' * (50 - calc_len(title))
    print(pattern % (push, title, padding, date, author))
#美化排版


url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
def fetch(url):
    response = requests.get(url, cookies={'over18':'1'})
    return response
#進到八卦版, 繞過年齡認證, 並取得html

def article(doc):
    html = HTML(html=doc)
    post = html.find('.r-ent')
    return post 
#定位到r-ent, 取得r-ent以下的資料

Page = int(input('Page =')) #讓user輸入讀取頁數, 並將user輸入的字串轉為int

res = fetch(url) 
post = article(res.text)
for entry in post: 
    pretty_print(entry.find('.nrec')[0].text, 
                 entry.find('.title')[0].text, 
                 entry.find('.author')[0].text, 
                 entry.find('.date')[0].text,
                 )
#排版並print

def get_pre_link(doc):
    html= HTML(html=doc)
    controls = html.find('.btn-group-paging .wide')[1]
    url = controls.attrs
    link = str('https://www.ptt.cc')+url['href']
    return link
#取得下一頁連結


print (Page)
if Page > 1: #頁數大於1才執行
    for loop in range(Page):
        pre_link = get_pre_link(res.text)
        resn = fetch(pre_link)  
        postn = article(resn.text)
        for ndata in postn:
            pretty_print(ndata.find('.nrec')[0].text, 
                         ndata.find('.title')[0].text, 
                         ndata.find('.author')[0].text, 
                         ndata.find('.date')[0].text,
                        )    
        res = resn
    #持續往前取得前一頁的資料
else:
    print("到此結束, 僅有一頁")