# pas
PAS (parsing and storing) reads large json files and stores them into a postgres database for later use (like machine learning)

I would suggest either using the Dockerfile or creating a virtual environment for ease of use.

#####Virtual Environment
1. virtualenv -p python3.6 venv_pas 
2. source venv_pas/bin/activate 
3. pip install -r requirements.txt 
4. python3 read_data.py
