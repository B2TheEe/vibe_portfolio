# vibe_portfolio

Een persoonlijke portfolio-website gebouwd met Django. De site is tweetalig (Nederlands/Engels) en bevat secties voor wie ik ben, mijn opleiding, werkervaring, vaardigheden, een blog en projecten.

## Functionaliteit

### Over mij
De homepage met een hero-sectie: profielfoto, titel, beschrijving en de mogelijkheid om het CV te downloaden (NL/EN). Daaronder een uitgebreide bio.

### Opleiding
Een tijdlijn van gevolgde opleidingen met instelling, beschrijving, start- en einddatum. Optioneel worden de propedeuse- en diplomadatum getoond.

### Werkervaring
Een tijdlijn van werkervaringen met bedrijf, functietitel, beschrijving en periode. Huidige functies worden als "Huidig" gemarkeerd.

### Vaardigheden
Vaardigheden gegroepeerd per categorie, elk met een icoon, beschrijving en een niveau-beoordeling op een schaal van 1 tot 5.

### Blog
Blogposts met een rijke teksteditor (CKEditor) en optionele afbeelding. Posts zijn te bekijken in een overzicht en een detailpagina. Ingelogde gebruikers kunnen posts aanmaken en bewerken.

### Portfolio
Een overzicht van GitHub-projecten met afbeelding, beschrijving en een directe link naar de repository.

## Technische details

- **Framework:** Django 4.2
- **Database:** SQLite
- **Talen:** Nederlands en Engels (via Django i18n + `i18n_patterns`)
- **Frontend:** Bootstrap 5, Bootstrap Icons, aangepast CSS met Python-kleurenschema
- **Rich text:** django-ckeditor

## Installatie

```bash
# Kloon de repository
git clone <repo-url>
cd vibe_portfolio

# Maak een virtuele omgeving aan en installeer dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Voer migraties uit
python manage.py migrate

# Compileer vertalingen
python manage.py compilemessages

# Maak een beheerdersaccount aan
python manage.py createsuperuser

# Start de ontwikkelserver
python manage.py runserver
```

Ga naar `http://127.0.0.1:8000/` voor de site en `http://127.0.0.1:8000/admin/` om content toe te voegen.
