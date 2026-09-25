# API REST ?tudiants

API de gestion d'un annuaire ?tudiant avec Flask, stockage en m?moire, tests pytest et contr?le qualit? flake8.

## Installation et lancement

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate
# macOS/Linux : source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app src.app run --debug
```

L'API ?coute par d?faut sur `http://127.0.0.1:5000`.

## Routes

- `GET /students?page=1&limit=10&sort=grade&order=desc` : liste, pagination et tri facultatifs.
- `GET /students/<id>` : d?tail d'un ?tudiant.
- `POST /students` : cr?ation JSON avec `firstName`, `lastName`, `email`, `grade` et `field`.
- `PUT /students/<id>` : remplacement valid? des donn?es de l'?tudiant.
- `DELETE /students/<id>` : suppression.
- `GET /students/stats` : statistiques g?n?rales.
- `GET /students/search?q=alice` : recherche par pr?nom ou nom, sans distinction de casse.

Champs autoris?s : `informatique`, `math?matiques`, `physique`, `chimie`. Les donn?es reviennent ? leur ?tat initial au red?marrage.

## Qualit?

```bash
pytest -q
flake8
```

GitHub Actions ex?cute le linter et les tests sur Python 3.10 et 3.11 pour chaque push et pull request vers `main`.
