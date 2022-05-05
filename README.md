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

The following data source was utilised as the target of the Web Scraping modules.

1. Primary Source - **hotcopper.com.au** Australia's largest stock  trading and investment forum


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

The first Workflow diagram demonstrates how the server and associated technologies interact to reach out to the hotcopper.com website and populate the database with ~1million rows of data. This data provides the data set for analysis. It was important to us to stick with our project goals of being the creator of the data set, and not rely on something pre existing. 

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


## Dashboard 

The primary user interface for this analytics tool is the **Raven Analytics** Dashboard. This Dashboard will provide users with a simple and clean UI for use. The following features are available in the current version of the application. As discussed previously the primary objective was to design, build an deploy the scalable infrastructure required to autonomously connect, store and make available the data scraped from financial web sites. 

With this now in place we have created a Dashboard which allows analysis of the following scenarios 

1.
2.
3.
4.



