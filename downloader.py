import os
import requests

import convert_par_v2
import convert_par_v3
import xmltool
import shutil


import argparse

# Initialize parser
parser = argparse.ArgumentParser(
                    prog='EBook-DL',
                    description='Downloads EBooks from sites in SVG format and converts them to PDF.',)

parser.add_argument('EBook_URL')  # positional argument
parser.add_argument('Login_URL')
parser.add_argument('Username')
parser.add_argument('Password')
parser.add_argument('-o', '--output')      # option that takes a value
args = parser.parse_args()

output_file_name = args.output

if not args.output:
    output_file_name = "output.pdf"

if not os.path.exists("downloaded"):
    os.makedirs("downloaded")


base_url = args.EBook_URL
svg_url=base_url+"{}.svg"
i = 1
payload={'email': args.Username,'password':args.Password}
print(payload)
s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',# This is another valid field
    'Content-Type': 'application/x-www-form-urlencoded'
}

log_req = s.post( args.Login_URL, data=payload, headers=headers)
xmltool.dl_req(svg_url.format(i), s)
while True:
    print(svg_url.format(i))
    data = s.get(svg_url.format(i))
    if data.status_code != 200:
        break
    open("downloaded/%d.svg" % i, "wb").write(data.content)
    xmltool.dl_img(data.text, s, base_url)
    print(f"File {i}.svg downloaded successfully!")
    i+=1


convert_par_v3.convert_to_pdf_fast(i-1, output_file_name)

shutil.rmtree("downloaded")