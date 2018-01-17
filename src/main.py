from flask import Flask, render_template, request, url_for, redirect
from schwifty import IBAN
import os
from functools import wraps

from render import latexify

app = Flask(__name__)
app.config.from_object('dev_config')

def auth_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != app.config['USER'] or auth.password != app.config['PASSWORD']:
            return "Kirjaudu sisään.", 401, {'WWW-Authenticate': 'Basic realm="Sisäänkirjautuminen vaaditaan."'}
        return f(*args, **kwargs)
    return wrapped

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def receive():
    errors = []
    bill = {}

    if len(request.form.get('nimi', '\0')) == 0:
        errors.append('Nimi on pakollinen kenttä.')

    try:
        IBAN(request.form.get('iban', '\0'))
    except ValueError:
        errors.append('IBAN ei ole validi.')

    if len(request.form.get('peruste', '\0')) == 0:
        errors.append('Maksun peruste tulee antaa.')

    if len(request.form.get('ids', '\0')) == 0:
        errors.append('Tositteita ei löytynyt.')

    if len(errors) > 0:
        return '\n'.join(errors), 400

    bill['nimi'] = request.form['nimi']
    bill['iban'] = request.form['iban']
    bill['peruste'] = request.form['peruste']
    bill['tositteet'] = []

    ids = request.form.get('ids', '\0').split(',')
    for id in ids:
        kuvaus = "kuvaus" + id
        liite = "liite" + id
        summa = "summa" + id

        if (not kuvaus in request.form) or (not summa in request.form) or (not liite in request.files):
            return 'Liiteistä puuttuu tietoja.', 400

        bill['tositteet'].append({
                'kuvaus': request.form[kuvaus],
                'liite': request.files[liite],
                'summa': request.form[summa]
            })

    ret = latexify(**bill)

    if not ret:
        return 'Kääntäminen epäonnistui.', 400

    return 'Lähettäminen onnistui.', 200

@app.route('/view', methods=['GET'])
@auth_required
def view():
    bills = os.listdir('src/static/bills')

    return "<br>".join(url_for('static', filename='bills/'+f) for f in bills), 200

@app.route('/static/bills/<fn>')
@auth_required
def download(fn):
    print(fn)
    return app.send_static_file('bills/' + fn)

if __name__ == '__main__':
    app.run()
