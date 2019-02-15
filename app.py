from flask import Flask, render_template
from flask_pymongo import flask_pymongo
import scrape_mars

app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def index():
    print("Server received request for 'Home' page...")
    return render_template('index.html')


# 4. Define what to do when a user hits the /about route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        [],
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
