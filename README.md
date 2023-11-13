# Freestoxx trade importer

Das Script liest einen Freestoxx Kontoauszug im **HTML**-Format ein und erzeugt aus den einzelnen Transaktionen (= ausgeführte Käufe / Verkäufe) die zusammengehörigen Trades.
Ein Trade gilt dann als geschlossen, wenn genau so viele Aktien eines Symbols verkauft wie zuvor gekauft wurden (bzw. entsprechend andersherum für SHORT-Trades).

Die Trades werden als SQLite Datenbank und CSV-Datei exportiert und können daraus in EXCEL importiert werden.

Die SQLite Datenbank wird als Zwischenspeicher benötigt. Diese stellt für das Script notwendige Funktionen bereit.


## Installation
Benötigte Software:
- Python Interpreter (https://www.python.org/downloads/windows/)

Vorgehen:
- Python installieren
- /setup/install_libs.bat ausführen


## Import der Daten
Test der Funktionionalität von Python und Script:
- do_import.bat ausführen
- In der CSV-Datei im Ordner /docs/example/ sollten jetzt drei Trades eingetragen sein.

realer Import:
- Datei user_config.json anpassen (enthält die Pfade & Dateinamen zum Kontoauszug, der SQLite Datenbank und der CSV-Datei.
- do_import.bat ausführen


## Einschränkungen

