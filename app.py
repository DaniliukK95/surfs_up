#9.4.3
#import dependencies for flask
from flask import Flask

#create flask app instance
app = Flask(__name__)

#create the 1st route
#define the starting point root. 
@app.route('/')
def hello_world():
    return 'Hello world'