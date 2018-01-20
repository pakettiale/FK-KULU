Tämä on Aalto-yliopiston Fyysikkokillan sähköinen kulukorvauslomake.

Asennusohjeet:

1. Lisää kansiot `bills` ja `tmp` ohjelman juureen.

2. Asenna python-riippuvuudet ajamalla `pip install -r requirements.txt` ja
`iban.js` ajamalla `git submodule update --init --recursive`.

3. Siirry virtualenv:iin `. bin/activate`.

4. Luo tietokanta seuraavasti: `cd src && python` ja 
```python
>>> from DB import db
>>> db.create_all()
```

Tämän jälkeen ohjelman voi ajaa komennolla `python src/main.py`. 
