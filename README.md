# World of Warcraft Commodities Analysis 📊

<br><img src="https://media.giphy.com/media/piTF2qfkyjpG4EB5Kk/giphy.gif" width="400"><br><br>

## What is it about❓

Blizzard recently made significant changes to the economy in World of Warcraft. Previously, each server had its own unique economy with varying market trends based on the in-game activities of players on that specific server. However, now commodities are traded region-wide, leading to increased availability of these items but also heightened competition.

This project aims to analyze commodity pricing and market trends in the in-game economy through a web application that serves as a service layer. The application will collect auction data using the WoW API, process the information to identify items with fluctuating prices and high trading volumes, and present this information to players in a user-friendly format. This will provide valuable insights for players seeking to make informed trades and stay ahead in the in-game economy.

## What should be the outcome? 💡

* A web application that collects and stores auction data for in-game commodities hourly using the WoW API.
* Automatically identifies items that fluctuate in price and are traded in large quantities on a weekly basis.

## Data Collection and Processing 🕸️

* Gather auction data for in-game commodities using the WoW API.
* Data includes item id, name, price, quantity and time left.
* Auction data enriched with quality, level, item class, item subclass, description and image.
* Clean and preprocess data to eliminate irrelevant or duplicate information.

## Time Series Analysis ⌚

* Track the price changes of individual items over time.
* Create a time series for each item and identify patterns such as weekly fluctuations.
* Analyze time series data to identify items that have a consistent pattern of fluctuation in price.

## Clustering 🪢

* Use a clustering algorithm to group similar items based on their price patterns.
* Identify items that are traded in large quantities within each cluster to find potentially profitable items to trade.

## Data Visualization 📈

* Present data in a meaningful way to allow users to easily identify items with consistent patterns of fluctuation in price.

## Skills utilized 🤹‍♀️

* Data collection (World of Warcraft API)
* Data cleaning (Python, Pandas)
* Data analysis (Time series analysis, Clustering)
* Data visualization (Matplotlib, Seaborn, ChartJS)

## Technologies used ⚙️

* SQL database (AWS)
* Backend (Django, Python)
* Frontend (JavaScript, HTML, CSS)

## Project management ✔️

* <a href="https://github.com/users/Senimtra/projects/6" target="_blank">GitHub Projects</a>
