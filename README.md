# EThOS-Project

Introduction and functionality description

The main objective of this tool is to assist a user in finding the most relevant theses to the user query in the Ethos database. This is achieved by using the modern NLP models for the sentence(s) embedding and semantic similarity search. 

The tool converts the user request into a vector and performs a semantic search based on the theses’ titles and abstracts embeddings. The five most relevant theses are then displayed to the user along with the results from the Ethos database for the same query. 

The user is then asked to score the tool response using the 1 to 10 scale and provide any other comments if needed. This feedback is stored in a database along with the query and tool response for further analysis and fine tuning of the tool hyper-parameters to improve its performance in the future. 
Required modules
The following Python modules need to be installed:
Flask
Numpy
Pandas
Sentence Transformers
Pymongo
Ssl
Mechanize
BeatifulSoup
Torch
flask_bootstrap

If you're using macOS then ensure that the certificates are installed  i.e. the "Install Certificates.command" file is run.

Additionally, the following pre-trained embeddings need to be downloaded:
abstract_embeddings(msmarco-distilbert-base-v4).pt
title_embeddings(msmarco-distilbert-base-v4).pt

Finally, MongoDB account needs to be set up if you would like to collect the search data and MongoDB Compass is recommended to be installed for managing the collected data. 
Implementation description
First, the UK Doctoral Thesis Metadata was downloaded from EThOS. The theses’ titles and abstracts then were embedded as vectors using msmarco-distilbert-base-v4 model from SBERT and stored for further use. 

Flask framework was used to create a simple web application and all the backend code was written using Python. MongoDB database was used to store queries, the tool responses and the user feedback on the tool result. MongoDB was chosen to allow flexibility in the data model as it’s expected that the database schema might need to be changed a few times to capture all the relevant information. MongoDB is also easier to use for data structures like Python lists and dictionaries, which are actively used in the tool back end. 

There are two Flask routes “/index” and “/results” that are served by the backend code that is split into two main packages:
Ethos_search: that retrieves the Ethos response to the user request and passes to the main application. This package uses mecanize and BeautifulSoup packages to communicate with the Ethos website as it doesn’t have a public API. 
Nlp_search: that embeds the user query using msmarco-distilbert-base-v4 model and than performs cosine similarity calculations, that is used as a measure of the semantic similarity between the user request and the titles and abstracts of all theses from the database to find the most relevant to the user request theses.
How to use?
Once installed, the main.py file needs to be run that starts the Flask application that can be accessed at http://127.0.0.1:5000/index. The user needs to input the query and click the ‘Submit’ button and then the tool displays the Ethos responses along with the semantic search results. 

The user is then encouraged to score the tool response using the 1 to 10 scale and provide any other feedback in the text field. 
