# Bachelorarbeit

Simulation zur Bachelorarbeit

## Allgemeines

- Student: Samir Faycal Tahar M'Sallem
- Thema: Dynamische Geschwindigkeitsempfehlung auf Basis von “vehicle-to-infrastructure” Kommunikation unter Einfluss von kollektiver Intelligenz zwischen Fahrzeugen 
- Abgabedatum: 


## Funktionsaufbau

### Kommunikationsnetzwerk 

- Fahrzeug zu Fahrzeug Kommunikation (mittels Datenstruktur (Shared Information Space))
- Fahrzeug zu Infrastruktur Kommunikation (mittels API)

### Informationen zur ausgewählten Kreuzung

- Position: 48.762205483237224, 11.428698086287278
- Intersection ID 1080: Schloßlände @ Schutterstraße
- https://goo.gl/maps/kb7ue8BfLkXTbvtM8
- http://personalsignal.traffictechservices.de/Home/Intersection?scnr=1080&region=Ingolstadt&groupId=511 **(nicht öffentlich zugänglich)**
- Approach 1 (links): latitude=48.76280618764156, longitude=11.427623411273599, direction=105.4492514593
- Approach 2 (geradeaus): latitude=48.763513657462475, longitude=11.431514833553978, direction=235.909123032
- Approach 3 (geradeaus, links): latitude=48.758733700993886, longitude=11.425519395220782, direction=40.2685517938


## Code

### Code/Ordner-Struktur


<pre>
simulation/
├─ README.md .............................. 
├─ launch.py .............................. # launchskript 
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


