import flask
from flask import request
import arrow
import config
import logging

app = flask.Flask(__name__)
CONFIG = config.configuration()

### Pages ###
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('welcome.html')

@app.route("/find-bathroom")
def find_bathroom():
    return flask.render_template('map.html')

@app.route("/add-bathroom")
def add_bathroom():
    return flask.render_template('add.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
