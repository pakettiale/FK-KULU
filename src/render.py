import shutil
import os
from datetime import datetime
import time
import texcaller
import jinja2
from werkzeug.utils import secure_filename
from subprocess import call, STDOUT

latex_jinja2_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('./src/templates'))
)

def latexify(nimi, iban, peruste, tositteet):
    base = secure_filename('{}-{}'.format(datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S"), texcaller.escape_latex(nimi)))
    folder = 'tmp/' + base + '/'
    os.mkdir(folder)

    print(os.getcwd())

    for tosite in tositteet:
        fn = folder + secure_filename(tosite['liite'].filename)
        tosite['liite'].save(fn)
        tosite['liite'] = fn
        print(fn)

    tositteet = [dict([(k, texcaller.escape_latex(v)) for (k,v) in t.items()]) for t in tositteet]

    template = latex_jinja2_env.get_template('template.tex')
    formatted = template.render(
        nimi=texcaller.escape_latex(nimi),
        iban=texcaller.escape_latex(iban),
        peruste=texcaller.escape_latex(peruste),
        tositteet=tositteet,
        yhteensa=sum(int(tosite['summa']) for tosite in tositteet)
    )

    print(formatted)

    texf = folder + base + '.tex'
    with open(texf, 'w') as f:
        f.write(formatted)

    # Kutsutaan kahdesti, jotta saadaan kuvat ja refit oikein
    dev = open(os.devnull, 'w')
    ret = call(['pdflatex', '-halt-on-error','-output-directory', folder, texf]) #, stdout=dev, stderr=STDOUT)
    ret |= call(['pdflatex', '-halt-on-error', '-output-directory', folder, texf], stdout=dev, stderr=STDOUT)

    if not ret:
        shutil.copy(folder + base + '.pdf', 'src/static/bills/')
    #shutil.rmtree(folder)

    return not ret
