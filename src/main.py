from flask import Flask, render_template, request
import validators

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

    if len(request.form.get('nimi', '\0')) == 0:
        errors.append('Nimi on pakollinen kenttä.')

    # Kuinka hyvin vastaa client-side validiointia?
    if not validators.iban(request.form.get('iban', '\0').replace(" ", "")):
        errors.append('IBAN ei ole validi.')

    if len(request.form.get('peruste', '\0')) == 0:
        errors.append('Maksun peruste tulee antaa.')

    if len(request.form.get('ids', '\0')) == 0:
        errors.append('Tositteita ei löytynyt.')

    if len(errors) > 0:
        return '\n'.join(errors), 405

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
            return ['Liiteistä puuttuu tietoja.'], 405

        bill['tositteet'].append({
                'kuvaus': request.form[kuvaus],
                'liite': request.files[liite],
                'summa': request.form[summa]
            })

    ret = latexify(**bill)

    if not ret:
        return ['Kääntäminen epäonnistui.'], 405

    return 'Success', 200

if __name__ == '__main__':
    app.run()
