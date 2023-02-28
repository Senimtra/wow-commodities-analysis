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

## Market Analysis ⌚

* Analyze market trends to identify patterns and fluctuations in supply and demand.
* Create charts to show number of items available, volumes traded, and market value.

## Item Distribution Analysis 🍰

* Create charts to show the distribution of each item against other relevant features such as sales volume and popularity.
* This will help players understand which items are in high demand and identify potential opportunities for profitable trades.

## Profitability Calculation 💰

* Calculate the profitability of each item based on traded quantities and market prices.
* Identify items that have high profitability and are currently underpriced in the market.

## Data Visualization 📈

* Present data in a meaningful way to allow users to easily identify items with consistent patterns of fluctuation in price.

## Skills utilized 🤹‍♀️

* Data collection (World of Warcraft API)
* Data cleaning (Python, Pandas)
* Data analysis (Time series analysis)
* Data visualization (Matplotlib, Seaborn, ChartJS)

## Technologies used ⚙️

* PostgreSQL database (AWS)
* Backend (Django, Python)
* Frontend (JavaScript, HTML, CSS)

## Project management ✔️

* <a href="https://github.com/users/Senimtra/projects/6" target="_blank">GitHub Projects</a>
