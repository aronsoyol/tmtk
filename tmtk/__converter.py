import requests
import bs4

session = requests.Session()


res = session.get("http://mtg.mglip.com/")

soup = bs4.BeautifulSoup(res.content, "html.parser")

form = soup.select("form")
form = form[0]

__VIEWSTATE = form.select("#__VIEWSTATE")[0].get("value")
__EVENTVALIDATION = form.select("#__EVENTVALIDATION")[0].get("value")

__post_data = {
    "__VIEWSTATE": __VIEWSTATE,
    "__EVENTVALIDATION": __EVENTVALIDATION,
    'ButtonTran_ID.x': 620,
    'ButtonTran_ID.y': 200
}


def convert2unicode(text):
    __post_data.update({"inputCyrillic_ID": text, })
    res1 = session.post('http://mtg.mglip.com/', data=__post_data)

    soup = bs4.BeautifulSoup(res1.content, "html.parser")
    outPutTraditonalM_ID = soup.select("#outPutTraditonalM_ID")

    return outPutTraditonalM_ID[0].text.strip("\r\n")
