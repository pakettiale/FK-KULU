Tämä on Aalto-yliopiston Fyysikkokillan sähköinen kulukorvauslomake.

Asennusohjeet:

1. Lisää kansiot `bills` ja `tmp`.

2. Asenna python-riippuvuudet ajamalla `pip install -r requirements.txt` ja
`iban.js` ajamalla `git submodule update --init --recursive`.

3. Siirry virtualenv:iin `. bin/activate`.

4. Lisää tietokanta, `cd src && python` ja 
`>>> from DB import db`
`>>> db.create_all()`
`guit()`


Ohjelman voi ajaa komennolla `python src/main.py`. 
