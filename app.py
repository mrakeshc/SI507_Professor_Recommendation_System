"""
Importing Flask and the tree object from the main python file
"""
from flask import Flask, render_template
from main import scraping_caching

#Creating an instance of the Flask class
app = Flask(__name__)

#Telling route() decorator what url should trigger our function
@app.route('/')
def index():
    data = scraping_caching()
    #Rendering the template using the tree data extracted
    return render_template('index.html', data=data)

#As usual main function call
if __name__ == "__main__":
    app.run(debug=True)
