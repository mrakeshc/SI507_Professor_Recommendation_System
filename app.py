from flask import Flask, render_template
from main import scraping_caching
app = Flask(__name__)


@app.route('/')
def index():
    data = scraping_caching()
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
