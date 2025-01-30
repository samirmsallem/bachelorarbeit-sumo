# Bachelorarbeit

Umsetzung der praktischen Forschungsarbeit mit Python innerhalb der Simulationsumgebung "Simulation of Urban MObility" (SUMO).

## Allgemeines

- Angestrebter Abschluss: Bachelor of Science
- Thema: Dynamische Geschwindigkeitsempfehlung auf Basis von “vehicle-to-infrastructure” Kommunikation unter Einfluss von kollektiver Intelligenz zwischen Fahrzeugen 

## Funktionsaufbau

### Kommunikationsnetzwerk 

- Fahrzeug zu Fahrzeug Kommunikation (mittels Datenstruktur (Shared Information Space))
- Fahrzeug zu Infrastruktur Kommunikation (mittels API)

### Informationen zur ausgewählten Kreuzung

- Es wurde eine Kreuzung ausgewählt, welche eine hohe Zuverlässigkeit hinsichtlich der Verfügbarkeit der Daten hat, sowie hinsichtlich der Datengenauigkeit (confidence level der Schaltzyklen)
- https://goo.gl/maps/kb7ue8BfLkXTbvtM8
- Position: 48.762205483237224, 11.428698086287278
- Content Provider interne Bezeichnung: Intersection ID 1080: Schloßlände @ Schutterstraße
- Approach 1 (links): latitude=48.76280618764156, longitude=11.427623411273599, direction=105.4492514593
- Approach 2 (geradeaus): latitude=48.763513657462475, longitude=11.431514833553978, direction=235.909123032
- Approach 3 (geradeaus, links): latitude=48.758733700993886, longitude=11.425519395220782, direction=40.2685517938


## Code

### Code/Ordner-Struktur


<pre>
simulation/
├─ README.md .............................. 
├─ projektbericht msallem.pdf ............. # Projektbericht der Projektphase
├─ bachelorarbeit.pdf ..................... # Bachelorarbeit
├─ launch.py .............................. # launchskript 
├─ requirements.txt ....................... # Python Module und Libraries 
├─ api/ ................................... # programmcode 
│  ├─ __init__.py ......................... 
│  ├─ output/ ............................. # enthält alle relevanten funktionen zur ausgabe auf der konsole oder als graphen
│  │  ├─ __init__.py ...................... 
│  │  ├─ logger.py ........................ # zentraler logger 
│  │  ├─ plotter.py ....................... # graph plotter
│  ├─ rest/ ............................... # enthält den rest-client für die Kommunikation mit der API, sowie die szenarien ordner
│  │  ├─ __init__.py ...................... 
│  │  ├─ client.py ........................ # rest-client zur verbindung mit der api
│  │  ├─ scenario1/ ....................... # enthält alle backend responses für das erste szenario
│  │  ├─ scenario2/ ....................... # enthält alle backend responses für das zweite szenario
│  │  └─ scenario3/ ....................... # enthält alle backend responses für das dritte szenario
│  ├─ sim/ ................................ # simulations handler
│  │  ├─ __init__.py ...................... 
│  │  ├─ helper.py ........................ # helper methoden die mittels traci modul auf simulationsdaten zugreifen
│  │  ├─ manager.py ....................... # main simulation manager (starten, beenden, steps)
│  │  ├─ visualizer.py .................... # visualizer zur erstellung von Kommunikationslinien (Polylines) zwischen Fahrzeugen und Ampeln (V2V bzw. V2I)
│  ├─ v2i/ ................................ # konkrete umsetzung der V2I Funktionalität
│  │  ├─ __init__.py ...................... 
│  │  ├─ glosa.py ......................... # berechnung und umsetzung der GLOSA
│  │  ├─ tli.py ........................... # Datenstruktur "TrafficLightInformation" zu Speicherung von V2I Responses
│  │  ├─ traffic_light.py ................. # Schaltverhalten der Ampelköpfe entsprechend der API-Daten
│  └─ v2v/ ................................ # konkrete umsetzung der V2V Funktionalität
│     ├─ __init__.py ...................... 
│     ├─ communication.py ................. # Kommunikationsaufbau zwischen Fahrzeugen
│     ├─ network.py ....................... # Generierung eines Fahrzeugnetzwerks (Bestimmung von Sendern und Empfängern)
│     ├─ signals.py ....................... # Enum welches die verwendeten Signale bündelt, die versendet werden können (innerhalb von V2V)
│     ├─ sis.py ........................... # Shared Information Space (Kommunikationsebene der Fahrzeuge), bündelt alle versendeten Nachrichtens
├─ docs/ .................................. # Anhang und Dokumente 
│  ├─ backend_response.json ............... # exemplarische Backend Response
│  ├─ glosa-improved-speed.png ............ # Geschwindigkeitsverhalten eines Fahrzeugs bei reiner V2I Nutzung
│  ├─ peaks from v2v move signal.png ...... # Geschwindigkeitsverhalten eines Fahrzeugs bei V2V2I Nutzung
│  ├─ unimproved-speed.png ................ # Geschwindigkeitsverhalten eines Fahrzeugs ohne Einfluss
│  ├─ v2v2i move + red signal.png ......... # Geschwindigkeitsverhalten eines Fahrzeugs bei V2V2I Nutzung
│  ├─ v2v2i-improved-speed.png ............ # Geschwindigkeitsverhalten eines Fahrzeugs bei V2V2I Nutzung
│  ├─ v2v2i-improved-speed2.png ........... # Geschwindigkeitsverhalten eines Fahrzeugs bei V2V2I Nutzung
│  └─ v2v2i-improved-speed3.png ........... # Geschwindigkeitsverhalten eines Fahrzeugs bei V2V2I Nutzung
├─ simulation/ ............................ # Konfigurationsdateien zur SUMO Simulation
│  ├─ osm.net.xml.gz ...................... # Netzwerkdefinition (Straßen, Lanes, Ampel)
│  ├─ osm.netccfg ......................... # Konfiguration
│  ├─ osm.poly.xml.gz ..................... # Umgebung um die Straßen
│  ├─ osm.polycfg ......................... # Konfiguration
│  ├─ osm_bbox.osm.xml.gz ................. # Konfiguration
│  ├─ routes.rou.xml ...................... # Definition der Routen und Fahrzeuge innerhalb der Simulation
│  └─ config/ ............................. # Start-Konfiguration
│     ├─ osm.sumocfg ...................... # Einbindung der Dateien und Konfigurationen
│     └─ osm.view.xml ..................... # Look and Feel innerhalb der Simulation
└─ simulation-output/ ..................... # Von der Simulation generierter Output (Graphen)
</pre>


### Installationshinweise

- Getestet wurde die Umgebung auf MacOSX mit Python 3.9
- SUMO Download und Installationshinweise: https://sumo.dlr.de/docs/Downloads.php
- **Bitte die SUMO_HOME Variable setzen!**
- Installierte SUMO Module: SUMO, SUMO-GUI, NETEDIT (zum Konfigurieren von `simulation/osm.net.xml.gz`)
- Python Module installieren: `pip install -r requirements.txt`


### Ausführung

- Sofern SUMO, Sumo-gui und die Python Module installiert wurden kann das Launch-Skript mittels `python launch.py` gestartet werden
- Der Befehl startet die SUMO Simulation mittels des "Traffic Control Interface" (TraCI) (https://sumo.dlr.de/docs/TraCI.html)
- Die Anwedung sumo-gui sollte sich öffnen und die Simulation starten

### Weitere Hinweise

- Der Code in `/api` greift mittels der TraCI API auf die Simulation zu und kann Simulations-Variablen abrufen und verändern
- TraCI baut eine Client-Server Architektur auf, wobei die Simulation als Server fungiert und der Code mittels des Clients ausgeführt wird
- Über den Python Code kann das Backend aufgerufen werden, welches über Ampelinformationen verfügt, die dazu notwendigen Daten (Position, usw.) werden mittels TraCI aus der Simulation extrahiert
- siehe: https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html und https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html sowie für Ampeln: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
- Die Backend Response enthält die Geschwindigkeitsempfehlung, wonach dann die Fahrzeuge gesteuert werden
- Sumo enthält von sich aus die Möglichkeit Fahrzeuge entsprechend von GLOSA bewegen zu lassen, da der Fokus auf der Nutzung von echten API Daten lag, wird diese Funktionalität nicht genutzt

