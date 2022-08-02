import sys, os
INTERP = "/home/avian_data/venv/bin/python"
os.environ["LANG"] ="C.UTF-8"
os.environ["LC_ALL"] = "C.UTF-8"
#INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)


from flask import Flask, redirect
from cloudfront.generate_cookie import generate_cookie
application = Flask(__name__)

@application.route('/')
def index():
    response = redirect("https://s3.avian-data.c-demo.xyz/index.html")
    cookies = generate_cookie.callback(url="https://s3.avian-data.c-demo.xyz/*", key="/home/avian_data/key/key.pem", key_id="K16V2XOUBQ6KK9")
    for name in cookies:
        response.set_cookie(name, cookies[name], domain=".avian-data.c-demo.xyz")
    return response
    
@application.route('/list_files.html')
def list_files():
    response = redirect("https://s3.avian-data.c-demo.xyz/list_files.html")
    cookies = generate_cookie.callback(url="https://s3.avian-data.c-demo.xyz/*", key="/home/avian_data/key/key.pem", key_id="K16V2XOUBQ6KK9")
    for name in cookies:
        response.set_cookie(name, cookies[name], domain=".avian-data.c-demo.xyz")
    return response

@application.route('/<first>/<path:rest>')
def all_others(first, rest):
    response = redirect("https://s3.avian-data.c-demo.xyz/{}/{}".format(first,rest))
    cookies = generate_cookie.callback(url="https://s3.avian-data.c-demo.xyz/*", key="/home/avian_data/key/key.pem", key_id="K16V2XOUBQ6KK9")
    for name in cookies:
        response.set_cookie(name, cookies[name], domain=".avian-data.c-demo.xyz")
    return response
    