# Pisos Scraper
Pràctica 1 de la UOC de l'assignatura M2.951 - Tipologia i cicle de vida de les dades.

## Membres del grup
1. Pau Campaña Soler

2. Edgar Ruben Pardo

## Descripció
Aquest programa extreu informació de la web https://pisos.com. Per cada pis, extreu diferents atributs. El resultat de l'execució del programa és un fitxer CSV on tens tots els pisos de la zona que desitges analitzar. El programa et dóna l'opció d'enviar el CSV al correu que desitgis.

## Com executar el programa
Tens dos opcions per executar el programa: 
### Executar-ho localment
Requisits: Cal tenir instal·lat python3, pip3, selenium y chromedriver.
Els passos per executar el programa són:
1. Per terminal, instalar els requirements: 
```
cd app
pip3 install -r requirements
```
2. Instalar pandas:
```
pip3 install pandas
```
3. Executar el programa:
```
cd src
python3 main.py
```

Els resultats de l'execució del programa estaran disponibles dins la carpeta `app/excels`

### Utilitzant Docker
Requisits: Cal tenir instal·lat docker.
Els passos per executar el programa són:
1. Construir la imatge:
```
docker image build . --tag pisos
```
2. Un cop esta construïda, executar el contenidor:
```
docker run pisos
```

## Parametrització del script

Hi ha diferents paràmetres  configurables que permeten modificar el comportament de l'execució. Aquests, es poden parametritzar des del fitxer `app/src/config.py`. Més informació a la [Wiki](https://github.com/paucampana/pisosScrapper/wiki).

## Llicència

Shield: [![CC BY-NC-ND 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY-NC-ND 4.0][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-black
