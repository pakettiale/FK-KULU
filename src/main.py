from flask import Flask, render_template, request
from schwifty import IBAN

from render import latexify

app = Flask(__name__)
app.config.from_object('dev_config')


@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def receive():
    errors = []
    bill = {}

    print('Helloo')

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

    return 'Success', 200

@app.route('/view', methods=['GET'])
def view():
    auth = request.authorization
    if not auth or auth.username != app.config['USER'] or auth.password != app.config['PASSWORD']:
        return "Please login.", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

    return "Woow", 200

if __name__ == '__main__':
    app.run()
