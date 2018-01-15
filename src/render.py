import shutil
import os
from datetime import datetime
import time
import texcaller
import jinja2
from werkzeug.utils import secure_filename
from subprocess import check_call, STDOUT

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

    for tosite in tositteet:
        fn = folder + secure_filename(tosite['liite'].filename)
        tosite['liite'].save(fn)
        tosite['liite'] = fn

    template = latex_jinja2_env.get_template('template.tex')
    formatted = template.render(
        nimi=texcaller.escape_latex(nimi),
        iban=texcaller.escape_latex(iban),
        peruste=texcaller.escape_latex(peruste),
        tositteet=[dict([(k, texcaller.escape_latex(v)) for (k,v) in t.items()]) for t in tositteet]
    )

    texf = folder + base + '.tex'
    with open(texf, 'w') as f:
        f.write(formatted)

    # Kutsutaan kahdesti, jotta saadaan kuvat ja refit oikein
    dev = open(os.devnull, 'w')
    check_call(['pdflatex', '-output-directory', folder, texf], stdout=dev, stderr=STDOUT)
    check_call(['pdflatex', '-output-directory', folder, texf], stdout=dev, stderr=STDOUT)
