from lxml import html, etree
import os


import requests
def parsehtml(html_data, session):
    # Parse the HTML
    print(html_data)
    tree = html.fromstring(html_data)


    # Extract the form
    form = tree.xpath("//form[@id='lti']")[0]
    action = form.attrib.get('action')
    method = form.attrib.get('method', 'get').lower()

    # Extract form inputs
    inputs = form.xpath(".//input[@name]")
    form_data = {i.attrib['name']: i.attrib.get('value', '') for i in inputs}
    #print(form_data)
    # Submit the form
    if method == 'post':
        response = session.post(action, data=form_data)
    else:
        response = session.get(action, params=form_data)

    if response.status_code != 200:
        return None
    # Print response
    print("Status Code:", response.status_code)
    print("Response URL:", response.url)
    print("Response Snippet:", response.text[:500])
    return response

def dl_req(site, session):
    req = session.get(site)
    print(req.text)
    if req.status_code != 200:
        return None
    else:
        req2 = parsehtml(req.text, session)
        if req2 is None:
            return None
        return parsehtml(req2.text, session)


def dl_img(svg_data, session, base_url):
    print(base_url)
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'xlink': 'http://www.w3.org/1999/xlink'
    }
    tree = etree.fromstring(svg_data.encode())
    images = tree.xpath('//svg:image', namespaces=namespaces)
    if len(images) != 0:
        path = images[0].get('{http://www.w3.org/1999/xlink}href') or images[0].get('href')
        path = os.path.dirname(path)
        if not os.path.exists("downloaded/"+path):
            os.makedirs("downloaded/"+path)

    for img in images:
        href = img.get('{http://www.w3.org/1999/xlink}href') or img.get('href')
        path = os.path.dirname(href)
        if not os.path.exists("downloaded/" + path):
            os.makedirs("downloaded/" + path)
        resp = session.get(base_url + href)
        print("downloaded/" + href)
        open("downloaded/" + href, "wb").write(resp.content)


