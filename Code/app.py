import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly
from wordcloud import WordCloud
from PIL import Image
import requests
import base64

plt.style.use('seaborn')

# Load environment variables
load_dotenv()

# Creds for PostgreSQL connection
sql_username=os.getenv("sql_username")
sql_pwd=os.getenv("sql_pwd")

# Create a connection to the database
engine = create_engine(f"postgresql://{sql_username}:{sql_pwd}@localhost:5432/hot_copper_db")

# Read in  hc_stock_sum table from the DB
hc_stock_sum_query = """
SELECT *
FROM hc_stock_sum
         """

# Read in  hc_top_likes table from the DB
hc_ticker_list_query = """
SELECT "0" as TICKER
FROM hc_ticker_list
         """

# Read in  hc_top_likes table from the DB
top_likes_query = """
SELECT
    b."Text", a."Ticker", a."Likes"
from
    hc_stock_sum a inner join hc_top_likes b on a."HREF_Link" = b."HREF" ORDER BY 3 DESC
         """

# Create a DataFrames from the query result
hc_stock_sum = pd.read_sql(hc_stock_sum_query, engine)
hc_ticker_list = pd.read_sql(hc_ticker_list_query, engine)
hc_top_likes = pd.read_sql(top_likes_query, engine)

# Charts (ADAM: postgres queries not working with direct column selects - e.g. select href from table)
top_tickers = hc_stock_sum[['Ticker','Likes']].groupby(
    'Ticker').sum().sort_values(
    by = 'Likes', ascending = False).head(10)


# SQL Query for tickers 
comments_trend = """
select
    count("HREF_Link") num_comments, 
    "Ticker"
from 
    hc_stock_sum
GROUP BY
    "Ticker", "Date"
ORDER BY 
    count("HREF_Link") DESC
FETCH FIRST 10 ROWS ONLY"""

# Read into df
comments_df = pd.read_sql(comments_trend, engine)
    
# Only get subset of hc_stock_sum as it is a large database
hc_stock_sum_ordered = hc_stock_sum.sort_values(by=['Likes'], ascending=False).head(10000)

# Drop unwanted columns
hc_stock_sum_ordered.drop(columns = 'Ticker_Filter', inplace = True)
########################################################################
# Streamlit Code

# Page layout
img = Image.open('Images/tab_logo.png')
st.set_page_config(page_title="Raven Analytics", layout = "wide", page_icon=img)
st.markdown("<h1 style='text-align: center; color: #3AE5E8; font-size:400%'>Raven Analytics</h1>", unsafe_allow_html=True)
st.markdown("We use the latest technology to create free tools for you to understand all the latest information being said about your ASX stocks.")

# Opening GIF file
file_ = open("Images/lottie_gif.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

_left, mid, _right = st.columns(3)
with mid:
    st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="logo">',
    unsafe_allow_html=True,
    )
    

# Split into two separate columns for Steamlit page layout
col1, col2 = st.columns(2)

# Initial column
with col1:

# Display all data from the database
    
    # Subheader
    st.subheader("Visualisation")
    
    # Markdown for header
    st.markdown("The following chart shows the most liked stocks based on comments made on stock forums.")
    
    # First chart for top 10 tickers with most likes
    top_likes_fig = st.bar_chart(data = top_tickers, use_container_width = True)
    
    # Print Streamlit Tables from Database
    st.markdown("The following shows the most liked comments on Hotcopper based on recent data collection.")
    st.write(hc_stock_sum_ordered)
    
    # Print Streamlit Tables from Database
    st.subheader("Hotcopper Tickers")
    st.write(hc_ticker_list)

    # Print Streamlit Tables from Database
    st.subheader("Hotcopper Top Likes")
    st.markdown("Browse the top comments on the HotCopper stock forums to see what investors deem to be useful information related to a stock.")
    st.write(hc_top_likes)
    
    # Subheader for most talked about
    st.subheader('Most active/talked about stocks')
    st.markdown('The following captures the stocks that are most talked about.')
    
    # Most talked about figure
    top_comments_fig = st.bar_chart(data = comments_df.set_index('Ticker'), use_container_width = True)
    
# Second column for selfe serve
with col2:
    
    # Subheading for SQL queries
    st.subheader("Self-Service Analytics:")
    
    # Markdown below subheader
    st.markdown("For users experienced in SQL (or who even want to learn), try querying our live database for information about your stock. Refer to the tables and data dictionaries below for further guidance.")
    
    # Tables
    st.markdown("""
    There are three tables used to store our data. These include :
     * **HC_STOCK_SUM**: Includes comment volume and likes about your stock including the poster and the HREF. Note that HREF is the key to joining to the comments table (sample query below)
     * **HC_TICKER_LIST**: Stuck on a ticker to search for? Refer to our database to find tickers for ASX companies. 
     * **HC_TOP_LIKES**: This table includes the comments that received the most likes from users on HotCopper. Use this table to join back to HC_STOCK_SUM
     
    Sample queries include:
     * `SELECT * FROM HC_STOCK_SUM FETCH FIRST 1000 ROWS ONLY` 
     * `SELECT * FROM HC_TOP_LIKES FETCH FIRST 1000 ROWS ONLY`
     * `SELECT "HREF" FROM HC_TOP_LIKES FETCH FIRST 1000 ROWS ONLY`
     * `SELECT a."Ticker", a."Poster", a."Likes", b."Text" from hc_stock_sum a inner join hc_top_likes b on a."HREF_Link" = b."HREF" ORDER BY 3 DESC FETCH FIRST 1000 ROWS ONLY`
     
    Note to user: when querying individual columns, ensure to place double quotations around the column name as per the last example above.
     """)
    
    # Create text input that is stored in variable for later use
    self_serve_query = st.text_input("For SQL users, input your own query here (table summary above):", max_chars = None)
    
    # Error handling for incorect queries
    try:
        
        # Take in query from text input
        user_query = self_serve_query
        
        # Create dataframe with the sql query
        output_user_query = pd.read_sql(user_query, engine)
        
        # Upon successful completion of the for loop, print successful query
        st.success("Query is valid. Please wait for your data.")
        
        # Additional features for dashboard functionality
        progress_bar = st.progress(0)
        
        # For loop for progress bar and printing successful query to user
        for percent_complete in range(100):
            
            # Time module for sleep
            time.sleep(0.1)
            
            # Add to progress bar
            progress_bar.progress(percent_complete + 1)
        
        # Output of results
        st.dataframe(output_user_query)
        
        
    # Raise exception if query did not run properly (generic error message)
    except:
        st.warning("Please try entering a valid query")
    
    # Next section for sentiment analysis
    st.subheader("ASX Stock Sentiment: What are investors saying about your stocks?")
    
    # Markdown
    ticker_input = st.text_input("Please enter a valid 3 letter ticker:")
    
    # Obtain text
    nlp_query = f"""
    SELECT
        b."Text", b."Tokenize"
    from
        hc_stock_sum a inner join hc_top_likes b on a."HREF_Link" = b."HREF"
    WHERE a."Ticker" = '{ticker_input}'
    """
    
    # Read into dataframe
    nlp_data = pd.read_sql(nlp_query, engine)
    
    try:
        
        # Display sample results
        st.dataframe(nlp_data)
        
        # Word cloud generation
        # Generate the words within the dataframe
        stock_words_list  = " ".join([str(x) for x in nlp_data['Tokenize']])

        # Generate the word cloud
        wc = WordCloud().generate(stock_words_list)
        
       
        # Show the image
        # Display the generated image:
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot(plt)
        
    except:
        
        st.warning("Please enter a valid ticker")
        
#############################################################
#Streamlit Network Code

import re
from pyvis.network import Network
import streamlit.components.v1 as components
import holoviews as hv
hv.extension('bokeh', logo=False)
import hvplot.pandas
from pathlib import Path

# Read in  asx200 table from the DB
asx200 = """
SELECT *
FROM asx200
         """

# Read in  shareholders table from the DB
shareholders = """
SELECT *
FROM shareholders
         """

# Read in  asx200 table from the DB
top20 = """
SELECT *
FROM top20
         """

st.markdown("## Full Network of Top 20 Shareholders of the ASX200")

# Helper functions
##############################################################
def extender_color_list(color_list, length_required):
    extended_color_list = []
    while True:
        for color in color_list:
            if len(extended_color_list) == length_required:
                return extended_color_list
            else:
                extended_color_list.append(color)
       
    

def string_cleaner(string, words_to_remove = []):
    string = str(string).lower()
    
    string = re.sub("<.+>|\(.+\)", "", string)
    
    string_list_space = string.split(" ")
    
    string_list = [word for word in string_list_space if word != ""]
    
    string_list_words_remove = [word.capitalize() for word in string_list if word not in words_to_remove]
    
    final_string = " ".join(string_list_words_remove)
    
    return final_string
                
def clean_up_df(df):
    # Drop empty cells
    df_drop = df.dropna()
    
    # Drop rows which have either:
        # No shareholder information 
        # No Top 20 shareholder information 
    # These are present in the Name column
    # But also present with 0 shares
    
    df_drop_0 = df_drop[df_drop["shares"] != 0]
    return df_drop_0
#################################################################

import pandas as pd
import re

#shareholders_df_raw = pd.read_csv("shareholders.csv")
shareholders_df_raw = pd.read_sql(shareholders, engine)
shareholders_df = clean_up_df(shareholders_df_raw)

ticker_asx200 = list(set(shareholders_df["ticker"]))

shareholders_clean = []
for shareholder in list(shareholders_df["name"]):
    shareholder_clean = string_cleaner(str(shareholder), ['custody', 'nominees', 'limited', 'pty', 'ltd'])
    shareholders_clean.append(shareholder_clean)
    
shareholders_df["Name_clean"] = shareholders_clean

unique_shareholders_asx200 = list(set(shareholders_df["Name_clean"]))

tickers_and_shareholders = ticker_asx200 + unique_shareholders_asx200

nodes_tickers_and_shareholders = list(range(len(tickers_and_shareholders)))

color_list = ["#FF0000", "#FFFFFF", "#00FFFF"
              , "#C0C0C0","#0000FF","#808080"
              ,"#00008B","#ADD8E6","#FFA500"
              ,"#800080","#A52A2A","#FFFF00"
              ,"#800000","#00FF00","#008000"
              ,"#FF00FF","#808000","#FFC0CB"]

extended_color_list = extender_color_list(color_list, len(tickers_and_shareholders))


# Creating the network
from pyvis.network import Network

net = Network(notebook = True, bgcolor="#222222", font_color="white")
#net = Network(notebook = True)

# Add specifications here
# Adding an additional node for ticker chosen
for node, color, label in zip(nodes_tickers_and_shareholders, extended_color_list, tickers_and_shareholders):
    # If label is a ticker in the ASX200
    if label in ticker_asx200:
        # Accessing names related to a ticker which is present in the form of 3 capital letters
        name_list = list(shareholders_df[shareholders_df["ticker"] == label]["Name_clean"])
        # Accessing capital percentage related to a ticker 
        capital_list = list(shareholders_df[shareholders_df["ticker"] == label]["capital"])
        
        title_node = f'{label} <br>Top 20 Shareholders:<br>'
        num = 0
        for shareholder, capital in zip(name_list, capital_list):
            num += 1
            title_node += f'<br>{num}) {shareholder}: {capital}'
            
        img = f"https://files.marketindex.com.au/xasx/96x96-png/{label.lower()}.png"
        
        # Creating the node
        net.add_node(n_id = node, label = label, title = title_node, image = img, shape = 'image')
        
    else:
        # Accessing names related to a non-asx200 company
        ticker_list = list(shareholders_df[shareholders_df["Name_clean"] == label]["ticker"])
        # Accessing capital percentage related to a company 
        capital_list = list(shareholders_df[shareholders_df["Name_clean"] == label]["capital"])
        
        title_node = f'{label} <br>Investments:<br>'
        num = 0
        for shareholder, capital in zip(ticker_list, capital_list):
            num += 1
            title_node += f'<br>{num}) {shareholder}: {capital}'
            
        # Creating the node
        net.add_node(n_id = node, color = color, label = label, title = title_node)
    

# Creating a dictionary to know which company is which node
company_nodes_dict = {}
for company, node in zip(tickers_and_shareholders, nodes_tickers_and_shareholders):
    company_nodes_dict[company] = node 

# Adding network edges for each company
for shareholder in unique_shareholders_asx200:
    shareholder_investments = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["ticker"])
    shareholder_investments_shares = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["shares"])
    shareholder_investments_capital = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["capital"])
    
    shareholder_node = company_nodes_dict[shareholder]
    for company, shares, capital in zip(shareholder_investments, shareholder_investments_shares, shareholder_investments_capital):
        company_node = company_nodes_dict[company]
        
        net.add_edge(shareholder_node, company_node, value = shares)
        
        
net.repulsion(node_distance=1500, spring_length=1000)
#path = '/tmp'
net.save_graph('../Html/pyvis_full_graph.html')

#path = '/tmp'
HtmlFile = open('../Html/pyvis_full_graph.html','r',encoding='utf-8')

if st.button("Display full network"):
    components.html(HtmlFile.read(), height=600, width = 2000)

def shareholders_connection_graph(ticker_chosen):
    
    #top20_raw = pd.read_csv("shareholders.csv")
    top20_raw = pd.read_sql(top20, engine)
    
    shareholders_df = clean_up_df(top20_raw)
    
    ticker_asx200 = list(set(shareholders_df["ticker"]))

    shareholders_clean = []
    for shareholder in list(shareholders_df["name"]):
        shareholder_clean = string_cleaner(str(shareholder), ['custody', 'nominees', 'limited', 'pty', 'ltd'])
        shareholders_clean.append(shareholder_clean)

    shareholders_df["Name_clean"] = shareholders_clean

    unique_shareholders_asx200 = list(set(shareholders_df["Name_clean"]))
    
    color_list = ["#FF0000", "#FFFFFF", "#00FFFF", "#C0C0C0","#0000FF","#808080","#00008B"
                  ,"#ADD8E6","#FFA500","#800080","#A52A2A","#FFFF00","#800000","#00FF00","#008000"
                  ,"#FF00FF","#808000","#FFC0CB"]
    
    

    
    # Specifying the number of nodes present in the selected network
    node_label = []
    for ticker in ticker_chosen:
        if ticker in ticker_asx200:
            # Ticker and their nodes
            list_of_shareholders = list(shareholders_df[shareholders_df["ticker"] == ticker]["Name_clean"])
            node_label += ([ticker] + list_of_shareholders)
        
        else:
            # Shareholders and their nodes
            list_of_shareholders = list(shareholders_df[shareholders_df["Name_clean"] == ticker]["ticker"])
            node_label += ([ticker] + list_of_shareholders)
            
    # Finalised node label related to tickers_chosen
    node_label = set(list(node_label))

    color_list = ["#FF0000", "#FFFFFF", "#00FFFF", "#C0C0C0","#0000FF","#808080","#00008B"
                  ,"#ADD8E6","#FFA500","#800080","#A52A2A","#FFFF00","#800000","#00FF00","#008000"
                  ,"#FF00FF","#808000","#FFC0CB"]
    
    # Creating length of color list required
    extended_color_list = extender_color_list(color_list, len(node_label))
    
    # Creating range of numbers for nodes
    node_num = list(range(len(node_label)))
    
    # Dictionary to access company's node number
    company_nodes_dict = {}
    
    # Setting up network
    from pyvis.network import Network

    net = Network(notebook = True, bgcolor="#222222", font_color="white")
    
    # Creating nodes related to tickers chosen
    for node, color, label in zip(node_num, extended_color_list, node_label):
    # If label is a ticker in the ASX200
        company_nodes_dict[label] = node
        if label in ticker_asx200:
            # Accessing names related to a ticker which is present in the form of 3 capital letters
            name_list = list(shareholders_df[shareholders_df["ticker"] == label]["Name_clean"])
            # Accessing capital percentage related to a ticker 
            capital_list = list(shareholders_df[shareholders_df["ticker"] == label]["capital"])

            title_node = f'{label} <br>Top 20 Shareholders:<br>'
            num = 0
            for shareholder, capital in zip(name_list, capital_list):
                num += 1
                title_node += f'<br>{num}) {shareholder}: {capital}'

            img = f"https://files.marketindex.com.au/xasx/96x96-png/{label.lower()}.png"

            # Creating the node
            net.add_node(n_id = node, label = label, title = title_node, image = img, shape = 'image')
        
        else:
            # Accessing names related to a non-asx200 company
            ticker_list = list(shareholders_df[shareholders_df["Name_clean"] == label]["ticker"])
            # Accessing capital percentage related to a company 
            capital_list = list(shareholders_df[shareholders_df["Name_clean"] == label]["capital"])

            title_node = f'{label} <br>Investments:<br>'
            num = 0
            for shareholder, capital in zip(ticker_list, capital_list):
                num += 1
                title_node += f'<br>{num}) {shareholder}: {capital}'

            # Creating the node
            net.add_node(n_id = node, color = color, label = label, title = title_node)

    
    # Adding network edges for each company
    for shareholder in ticker_chosen:
        if shareholder in ticker_asx200:
            shareholder_investments = list(shareholders_df[shareholders_df["ticker"] == shareholder]["Name_clean"])
            shareholder_investments_shares = list(shareholders_df[shareholders_df["ticker"] == shareholder]["shares"])
            shareholder_investments_capital = list(shareholders_df[shareholders_df["ticker"] == shareholder]["capital"])

        else:
            shareholder_investments = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["ticker"])
            shareholder_investments_shares = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["shares"])
            shareholder_investments_capital = list(shareholders_df[shareholders_df["Name_clean"] == shareholder]["capital"])
            
        shareholder_node = company_nodes_dict[shareholder]
        for company, shares, capital in zip(shareholder_investments,shareholder_investments_shares,shareholder_investments_capital):
            company_node = company_nodes_dict[company]
            
            net.add_edge(shareholder_node, company_node, value = shares)

    net.repulsion(node_distance=300, spring_length=200)
    #path = '/tmp'
    net.save_graph('../Html/pyvis_graph.html')

col1, col2 = st.columns(2)

#top20_raw = pd.read_csv("shareholders.csv")
top20_raw = pd.read_sql(shareholders, engine)

shareholders_df = clean_up_df(top20_raw)


# Select ticker
ticker_list = list(set(shareholders_df["ticker"]))
selected_ticker = st.multiselect('Select ticker(s) to visualize', ticker_list)



# Select shareholder
shareholders_list = []
for shareholder in list(shareholders_df["name"]):
    shareholder_clean = string_cleaner(str(shareholder), ['custody', 'nominees', 'limited', 'pty', 'ltd'])
    shareholders_list.append(shareholder_clean)
        
selected_shareholder = st.multiselect('Select Shareholder(s) to visualize', list(set(shareholders_list)))

# Combine both
ticker_and_shareholder = selected_ticker + selected_shareholder


shareholders_connection_graph(ticker_and_shareholder)

#path = '/tmp'
HtmlFile = open('../Html/pyvis_graph.html','r',encoding='utf-8')



components.html(HtmlFile.read(), height=600, width = 2000)
    
    
def display_tables(ticker_chosen):
    #top20_raw = pd.read_csv("shareholders.csv")
    top20_raw = pd.read_sql(shareholders, engine)
    
    # Drop rows with no information
    shareholders_df = clean_up_df(top20_raw)
    
    name_clean = []
    for name in list(shareholders_df.name):
        name_clean.append(string_cleaner(name, ['custody', 'nominees', 'limited', 'pty', 'ltd']))
        
    shareholders_df["Name_clean"] = name_clean
    
    # Set up list of tickers with information for use
    ticker_asx200 = list(set(shareholders_df["ticker"]))
    
    displayed_list = []
    for ticker in ticker_chosen:
        # If ticker chosen is a ASX200 company
        if ticker in ticker_asx200:
            ticker_df = shareholders_df[shareholders_df["ticker"] == ticker]
            displayed_list.append(ticker_df)
        # If ticker chosen is a shareholder of an ASX200 company
        else:
            ticker_df = shareholders_df[shareholders_df["Name_clean"] == ticker]
            displayed_list.append(ticker_df)
            
    df = pd.concat(displayed_list, axis = 0)
    df = df[["name", "shares", "capital", "ticker"]].set_index("name")
    return df

try:
    st.sidebar.table(display_tables(ticker_and_shareholder))
except:
    st.sidebar.write("Table displayed here")


import re
import hvplot.pandas
def graph_insider(ticker_chosen):
    import re
    import hvplot.pandas
    
    insider_df = pd.read_csv("insider.csv")
    
    insider_df["Date"] = pd.to_datetime(insider_df["Date"])
    
    price_list = list(insider_df.Value)
    
    # Change values from string to float numbers
    int_price_list = []
    for price in price_list:
        if re.findall("\(", price):
            # Removing , from values
            price = re.sub(",", "", price)
            # Removing () and $ from negative numbers
            int_price_list.append(float(price[2:-1]))
        else:
            # Removing , from values
            price = re.sub(",", "", price)
            # Removing $ from positive numbers
            int_price_list.append(float(price[1:]))
            
    insider_df["Bought/Sold"] = int_price_list
    
    # Filter for selected tickers
    hvplot_str_list = []
    for ticker in ticker_chosen:
        hvplot_str_list.append(f'insider_df[insider_df["ticker"] == "{ticker}"].sort_values(by = ["Date"]).set_index("Date").hvplot.bar(y = "Bought/Sold", hover_cols = ["Director", "Price", "Value", "Type"], rot = 90, shared_axes = False, title = f"{ticker} Insider trades")')
        
    hvplot_str = " + ".join(hvplot_str_list) 
    return eval(hvplot_str)

try:
    graph = graph_insider(selected_ticker)
    hv.save(graph ,'fig.html')
    HtmlFile = open("fig.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=1800, height=1200, scrolling=True)
except:
    pass
