# Pisos Scrapper
Pràctica 1 de la UOC de l'assignatura Tipologia i cicle de vida de les dades.

## Membres del grup
Pau Campaña Soler
Edgar Ruben Pardo

## Descripció
Aquest programa extreu informació de la web https://pisos.com. Per cada pis, extreu diferents atributs. El resultat de l'execució del programa és un fitxer CSV on tens tots els pisos de la zona que desitges analitzar. El programa et dóna l'opció d'enviar el CSV al correu que desitgis.

## Com executar el programa
Tens dos opcions per executar el programa: 
### Executar-ho directament
Requisits: Fa falta tenir instalat python3, pip3, selenium y chromedriver.
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
Requisits: Fa falta tenir instalat docker.
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

Hi ha diferents paramentres que es poden configurar des del fitxer `app/src/config.py`:

| Atribut   |      Valor per defecte      |  Descripció |
|----------|:-------------:|------:|
| URL_PISOS |  https://www.pisos.com | Url de la web que es vol fer webscrapping (No s'hauria de modificar) |
| URL_PLACE |    /venta/pisos-esparreguera/   |   Zona de la qual es vol fer l'estudi |
| URL_LOG_IN | https://www.pisos.com/Login |   Url de la pàgina per fer log in |
| USER_PISOS |  informe.casas@gmail.com | Nom de l'usuari amb el que es vol fer log in a pisos.com |
| PW_PISOS |    XXXXXX   |   Contrassenya de l'usuari amb el que es vol fer log in a pisos.com |
| SMTP_SERVER | smtp.gmail.com |    Servidor per enviar el correu |
| SMTP_PORT |  587 | Port del servidor per enviar el correu |
| MAIL_TO_SEND |    informe.casas@gmail.com   |   Correu on es vol enviar el fitxer CSV |
| TEST_MODE | False |  Atribut per fer tests. En el cas de que nomes es vulgui es fer l'estudi d'un sol pis, posar valor a True  |
| MAX_WORKERS |  1 | Número de workers per fer el webscrapping dels pisos. Ho fa de manera paral·lela |
