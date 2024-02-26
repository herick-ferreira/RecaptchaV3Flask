from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pytz import timezone
from werkzeug.middleware.proxy_fix import ProxyFix
import app_config
import requests
from warnings import filterwarnings



filterwarnings('ignore')

app = Flask(__name__)
app.config.from_object(app_config)

tz = timezone('Brazil/East')
year = f'{datetime.now(tz=tz):%Y}'

SITE_KEY = app.config["SITE_KEY"]
app.secret_key =  app.config["SECRET_SESSION"]

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)




@app.errorhandler(404)
def page_not_found(e):
    return "Page doesn't exists"


# ROTAS

@app.route("/")
def page_home():
    return render_template('contact.html', SITE_KEY=app_config.SITE_KEY, year=year)




@app.route('/add-contact', methods=["GET", "POST"]) 
def add_contact(): 


    if request.method == "GET": return jsonify({'message':'Send Post Method'})

    data = request.get_json()

    secret_response = data['g-recaptcha-response']

    SECRET_KEY = app_config.SECRET_KEY
    VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

    verify_response = requests.post(f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}')

    if verify_response.status_code != 200:
        print(f"Unable to authenticate with this user... - {datetime.now(tz=tz):%d/%m/%Y %H:%M:%S}")
        return jsonify({'message':'False'})

    if not 'success' in verify_response.json().keys():
        print(f"Unable to authenticate with this user... - {datetime.now(tz=tz):%d/%m/%Y %H:%M:%S}")
        return jsonify({'message':'False'})

    if not verify_response.json()['success'] or verify_response.json()['score'] < 0.5:
       return jsonify({'message':'False'})
    

    return jsonify({'message':'True'})






if __name__ == '__main__':
     app.run(debug=False)
