# Pisos Scrapper
Pràctica 1 de la UOC de l'assignatura M2.951 - Tipologia i cicle de vida de les dades.

## Membres del grup
1. Pau Campaña Soler

2. Edgar Ruben Pardo

## Descripció
Aquest programa extreu informació de la web https://pisos.com. Per cada pis, extreu diferents atributs. El resultat de l'execució del programa és un fitxer CSV on tens tots els pisos de la zona que desitges analitzar. El programa et dóna l'opció d'enviar el CSV al correu que desitgis.

## Com executar el programa
Tens dos opcions per executar el programa: 
### Executar-ho localment
Requisits: Cal tenir instalat python3, pip3, selenium y chromedriver.
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

Els resultats de l'execució del programa estaràn disponibles dins la carpeta `app/excels`

### Utilitzant Docker
Requisits: Cal tenir instalat docker.
Els passos per executar el programa són:
1. Construir la imatge:
```
docker image build . --tag pisos
```
2. Un cop esta construida, executar el contenidor:
```
docker run pisos
```

## Parametres que es poden configurar

Hi ha diferents paràmetres  configurables que permeten modificar el comportament de l'execució. Aquests, es poden parametritzar des del fitxer `app/src/config.py`. [Wiki] (https://github.com/paucampana/pisosScrapper/wiki)
