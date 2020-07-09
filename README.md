# OSM Service

Der Open Street Map Service bietet eine REST-API an, welche interessante Datenpunkte aus dem Datenstand von [Open Street Map](https://www.openstreetmap.org/) (OSM) extrahiert und zu der weiteren Verarbeitung zurückgibt.

![API Dokumentation](/screenshots/parks_und_drogerien_visualized.jpg)

Die Daten werden in einem übergebenen Umkreis relativ zu einer gegebenen Koordinate zurückgegeben.

Die folgenden Daten können extrahiert werden:
- ÖPNV
    - Bahnhöfe
    - Tram-Stationen
    - Bus-Stationen
- Typ des Umfelds
    - Fußgängerzone
    - Bürokomplex
    - Wohngegend
    - Industrie Gebiet
- Parkplatzsituation
- öffentliche Parks
- Shops
    - Malls
    - Drogerien
    - Gemischtwarenladen
    - Supermärkte
- Öffentliche Einrichtungen
    - Schulen
    - Kindergärten
    - Krankenhäuser
    - Arztpraxen

## Datenbank
Der Service benötigt eine Datenbank in der die Open Street Map Daten hinterlegt werden, um diese schnell extrahieren zu können.

Es wurde sich für [PostgreSQL](https://www.postgresql.org/) entschieden, welches ein kostenloses Open-Source Datenbankmanagementsystem ist.
Damit PostgreSQL die geografischen Daten von Open Street Map speichern und verbreiten kann, wird zusätzlich das kostenlose [PostGIS Erweiterungspaket](https://postgis.net/) benötigt.

Im `database/` Ordner befindet sich eine `docker-compose` Konfigurations Datei welche einen PostGIS Datenbank Container definiert. Diese kann mit `sudo docker-compose --file ./database/docker-compose.yml up` gestartet werden.
Das Standardpasswort ist `password` und sollte vor der Nutzung abgeändert werden.

Alternativ kann auch eine bestehende PostgreSQL/PosGIS Installation genutzt werden.

Um die OSM Daten in die Datenbank zu laden kann man das Program `ogr2ogr` benutzen. Dies ist ein Teil des Software Pakets [GDAL](https://gdal.org/index.html). Im `database/` Ordner gibt es dafür das `import_data.sh` Script welches die OSM Daten aus Nordrhein-Westfalen mit `ogr2ogr` in die Datenbank lädt. Auf [geofabrik.de](http://download.geofabrik.de/) kann man sich die OSM Daten als `.osm.pbf` beliebiger Regionen der Erde herunterladen.

## Webserver

Der Webserver implementiert eine REST-API mit dem Python Webframework [Flask](https://palletsprojects.com/p/flask/).

Eine API Dokumentation wird automatisch generiert und ist unter der URL Wurzel erreichbar. Dort werden alle vorhandenen Endpunkte aufgelistet und können live getestet werden.
![API Dokumentation](/screenshots/api_documentation.png)

Die Datenbankverbindungsinformationen lassen sich in der `settings.cfg` Datei anpassen.

Die Flask App kann mit allen Web Server Gateway Interface (WSGI) kompatiblen Webservern gehostet werden.

Zum Beispiel mit [gunicorn](https://gunicorn.org/):
- `cd webserver`
- `SETTINGS_FILE=settings.cfg gunicorn --bind 0.0.0.0:5000 wsgi:app`

Ein Debug Server lässt sich auch folgendermaßen starten:
- `cd webserver`
- `FLASK_APP=webserver.py SETTINGS_FILE=settings.cfg flask run`
