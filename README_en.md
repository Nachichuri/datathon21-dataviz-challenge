# Campus Party 2021 - Datathon TELECOM 2021
## :chart_with_upwards_trend:  [Data Viz Challenge](https://github.com/Datathon2021/data-viz) :chart_with_downwards_trend:
Lee este documento en [Español]().

---

## :thought_balloon: 1. Challenge information:
During 2021 Campus Party edition, TELECOM company launched an open Data Challenge with the following mission:

**Using a dataset containing Flow Platform's view history, create an effective visualization that helps understand and/or describe the dataet and get insights.** (Flow is Telecom's on-demand content platform with movies, series and TV shows.)
*Utilizando un conjunto de datos sobre el historial de visualizaciones de clientes en la plataforma Flow: “Armar una visualización efectiva que ayude a entender/describir el data set y obtener insights”*

## :running: 2. Execution:
To solve the challenge, I made a visualization panel that shows daily and monthly stats about the content watched on the platform:

### :suspect: Access: http://143.198.181.204:3569/

![](assets/overview.gif)

The provided datasets contain a ton of information, so I prioritized the graphs I considered more useful, and worked both on said graphs' filtering functions and the data presentation itself. There's actually a lot more of information available to keep feeding the panel with more stats.

## :wrench: 3. Tools used:
The main programming language used is Python. I created an interactive [Dash](https://dash.plotly.com/introduction) panel, containing [Plotly](https://plotly.com/python/plotly-express/) graphs which are fed by [Pandas](https://pandas.pydata.org/about/) DataFrames, filtered to get the required datasets. What's good about using technologies like Pandas is that with few source code modifications, you can get the dashboard information for a dataset returned from a database, datalake or API.

## :chart_with_upwards_trend: 4. Panel access:
### **Option 1 - Online**
The panel will be online until the Datathon's closing day, hosted on a DO droplet at:
- [143.198.181.204:3569 (FLOW)](http://143.198.181.204:3569/)
### **Option 2 - Local execution**
1. Create a new directory and clone this repo:

```bash
git clone https://github.com/Nachichuri/datathon21-dataviz-challenge.git
```
2. (Opt.) Create a virtual environment:

```bash
pip install virtualenv
virtualenv venv
```

3. Install required libraries:

```bash
cd datathon21-dataviz-challenge/
pip install -r requirements.txt
```

4. Unzip the main dataset in the data/ folder

```bash
unzip data/train.csv.zip data/
```

5. Run tests to see everything is working as planned

```bash
pytest
```

6. Run Dash's development server 

```bash
python index.py
```

#### All done! You can access the panel writing [localhost:3569 (FLOW)](http://localhost:3569/) on your browser.

## :mailbox_with_mail: 5. Reach out:
You can reach me at nachichuri@gmail.com or @nachichuri in Telegram :smile: