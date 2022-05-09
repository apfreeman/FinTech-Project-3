# FinTech-Project-3

# Project Title
## Raven Analytics

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/How-Data-Analytics.jpg?raw=true)

# Team Members

- Jordan Dass
- Adam Freeman 
- Mitchell Langdon 
- Tracey Martin
- Marcus Whitelock 

# Project Description/Outline

As the final project of this Fintech Bootcamp Course our team has selected the sub category of analytics. For this project our team has created an Web Data collection and Analytics solution designed to enable the autonomous gathering of information posted or appearing on any targeted website. 

Our primary focus was to dig deeper then what is a traditional black box solution such as a market API to return market sentiment data, instead opting to undertake a significantly more challenging task of sourcing and storing the data ourselves. By controlling the sourcing of this data we believe we are able to build an agile solution allowing infinite future growth and development as new requirements and opportunities develop.

This approach while more challenging was a deliberate decision based on two main factors 
    
1. The lack of good sentiment API for ASX listed companies specific to our needs
2. The inflexible nature and lack of granularity and integration when using off the shelf solution (API, Mailing list etc).

To achieve this goal we have designed an end to end solution with the following deliverables.

1. Continuous Web Scraping data gathering
2. Data cleaning, processing and storage
3. Data analysis 
4. Self service data analytics tool

The focus of this project is heavily weighted towards building the core infrastructure to allow the unattended collection, storing and hosting of the collected data that would allow it to be a single point of truth that could be reused for analysis. While only limited analysis is available via the dashboard, this solution has been architected such that it can scale up significantly to collect more data from more sources.  

## Data Sources 

The following data sources have been utilised as the target of the Web Scraping modules. This solution is not limited to these sources, any web source could be used.

1. Source 1 - **hotcopper.com.au** Australia's largest stock  trading and investment forum

2. Source 2 - **marketindex.com.au** Financial portal for the Australian stock market. Up-to-date ASX market analysis, share prices, charts and index performance data.


## High Level Solution Design and Workflows

The solution will consist of the following components. These technologies will be combined on a Windows Server to allow 24x7 always on data collection and analysis. 

1. Data Collector (Selenium)
2. Data Aggregator (Pandas/CSV)
3. Data Storage (SQL)
4. Analysis (Python)
5. WebApp UI (Streamlit)

The following section will detail the high level solution design along with some key workflows 

### Solution Overview

The diagram below details the high level solution design along with the technologies utilised at each layer. All layers of this solution including infrastructure have been built by the team from scratch.

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/app_architecture_only.png?raw=true)

### Workflow 1 - Python and Selenium to scrape web data

The first Workflow diagram demonstrates how the server and associated technologies interact to reach out to the hotcopper and marketdata websites and populate the database with more than 1million rows of data across 6 tables. This data provides the data set for analysis. It was important to us to stick with our project goals of being the creator of the data set, and not rely on something pre existing. 

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/app_workflow_1.PNG?raw=true)

### Workflow 2 - Use Database, Python, and Selenium to scrape forum comments

The second Workflow diagram demonstrates how the solution uses the populated database to reach out and gather additional layers of information that has been targeted by user interaction or  specific requirement. 

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/app_workflow_2.PNG?raw=true)

### Workflow 3 - Use Database and Python to create analysis and visualisations

The third Workflow demonstrates how the solution with a populated dataset can now produce analysis and visualisations using common python libraries. 

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/app_workflow_3.PNG?raw=true)

### Workflow 4 - Use Database, Python and Streamlit to create user interface

The fourth Workflow demonstrates how a user will interface with the solution. It is intended that all infrastructure is hidden from the user, with just a single point of entry using a web browser accessible dashboard for a clean and simple user experience. An end user will be able to access reports or other information and even self serve particular requests based on their own requirements. 

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/app_workflow_4.PNG?raw=true)


## User Interface 

***NOTE: This system runs on paid infrastructure and as such has been stopped after demo to stop incurring costs. If for marking ths UI needs to be live, please slack Adam Freeman to start.*** 

The primary user interface for this analytics tool is the **Raven Analytics** Dashboard - [Link to Raven Dashboard](http://raven.creativenetworks.com.au:8502/). This Dashboard will provide users with a simple and clean UI for use and is available on PC and mobile. The following features are available in the current version of the application. As discussed previously the primary objective was to design, build an deploy the scalable infrastructure required to autonomously connect, store and make available the data scraped from financial web sites. 

With this now in place we have created a UI Dashboard which allows analysis of the following scenarios. Despite the examples, the possibilities going forward as an analysis tool are endless.   

1. Visualisation

The following charts show the most liked stocks based on comments made on stock forums.

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/1_visualisation.PNG?raw=true)

2. Self-Service Analytics

For users experienced in SQL (or who even want to learn), try querying our live database for information about your stock. Refer to the tables and data dictionaries below for further guidance.

There are three tables used to store our data. These include :

- HC_STOCK_SUM: Includes comment volume and likes about your stock including the poster and the HREF. Note that HREF is the key to joining to the comments table (sample query below)

- HC_TICKER_LIST: Stuck on a ticker to search for? Refer to our database to find tickers for ASX companies.

- HC_TOP_LIKES: This table includes the comments that received the most likes from users on HotCopper. Use this table to join back to HC_STOCK_SUM

Query example

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/2_ss_analytics.PNG?raw=true)

3. Hotcopper Tickers

A scrollable table of all tickers data has been collected for (2110)

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/3_hc_tickers.PNG?raw=true)

4. Hotcopper Top Likes

Browse the top comments on the HotCopper stock forums to see what investors deem to be useful information related to a stock.

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/4_hc_top_likes.PNG?raw=true)


5. ASX Stock Sentiment: What are investors saying about your stocks?

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/5_sentiment.PNG?raw=true)

6. Most active/talked about stocks
The following captures the stocks that are most talked about.

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/6_most_active.PNG?raw=true)


7. Full Network of Top 20 Shareholders of the ASX200

See the relationships between asx200 stocks and the top 20 shareholders.

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/network_capture.gif?raw=true)

8. Custom filter for Stocks and Shareholders

Filter down these relationships using custom selections

![](https://github.com/apfreeman/FinTech-Project-3/blob/main/Images/8_custom_filter.PNG?raw=true)
