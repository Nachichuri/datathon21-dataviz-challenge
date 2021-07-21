# Campus Party 2021 - Datathon TELECOM 2021
## :chart_with_upwards_trend:  [Data Viz Challenge](https://github.com/Datathon2021/data-viz) :chart_with_downwards_trend:
Read this document in [English]().

---

## :thought_balloon: 1. Información del desafío :
Enmarcado en la Campus Party 2021, TELECOM realizó un Data Challenge abierto con la siguiente consigna:

*Utilizando un conjunto de datos sobre el historial de visualizaciones de clientes en la plataforma Flow: “Armar una visualización efectiva que ayude a entender/describir el data set y obtener insights”*

## :running: 2. Ejecución:
Para resolver el desafio se armó un panel informativo que permite acceder a estadísticas diarias y mensuales sobre el contenido consumido en la plataforma:

### :suspect: Acceso al panel: http://143.198.181.204:3569/

![](assets/overview.gif)

Si bien los datasets usados para el desafio tienen información muy variada y rica, se definieron visualizaciones prioritarias y se trabajó en pulir los algoritmos de filtrado y la presentación de resultados. Hay muchísima más información disponible para explotar y seguir nutriendo el panel.

## :wrench: 3. Herramientas utilizadas:
El desafio se resolvió con Python, utilizando un panel de [Dash](https://dash.plotly.com/introduction), el cual muestra graficos de [Plotly](https://plotly.com/python/plotly-express/) alimentados por DataFrames de [Pandas](https://pandas.pydata.org/about/) filtrados para lograr el set de datos deseado. Lo bueno de usar tecnologías como Pandas es que con muy pocas modificaciones en el codigo, se puede obtener el contenido filtrado de los datasets directamente desde una API o una base de datos, y poder procesar toda la informacion disponible.

## :chart_with_upwards_trend: 4. Acceso al panel:
### **Opción 1 - Online**
Hasta la finalización de la Datathon estará disponible para su consumo en un droplet con la siguiente direccion:
- [143.198.181.204:3569 (FLOW)](http://143.198.181.204:3569/)
### **Opcion 2 - Ejecución local**
1. Creá un nuevo directorio y cloná este repositorio:

```bash
git clone https://github.com/Nachichuri/datathon21-dataviz-challenge.git
```
2. (Opcional) Creá un virtual environment:

```bash
pip install virtualenv
virtualenv venv
```

3. Instalá las librerias requeridas:

```bash
cd datathon21-dataviz-challenge/
pip install -r requirements.txt
```

4. Descomprimí el dataset de visualizaciones en la carpeta data/

```bash
unzip data/train.csv.zip data/
```

5. Probá que todo este en orden

```bash
pytest
```

6. Ejecutá el servidor de pruebas

```bash
python index.py
```

#### Listo! Podés acceder entrando a [localhost:3569 (FLOW)](http://localhost:3569/).

## :mailbox_with_mail: 5. Contacto:
Podés escribirme con dudas, consultas o sugerencias a nachichuri@gmail.com o @nachichuri en Telegram :smile: