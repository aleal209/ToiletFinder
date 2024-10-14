"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import config

import logging

### Globals ###
app = flask.Flask(__name__)
CONFIG = config.configuration()

### Pages ###
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

###############
# AJAX request handlers
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times based on kilometers, start time, and control distance.
    Expects URL-encoded arguments: km, start_time, and control_distance.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', type=float)
    start_time = request.args.get('start_time', arrow.now().isoformat)
    control_distance = request.args.get('control_distance', 200, type=int)

    app.logger.debug("km={}, start_time={}, control_distance={}".format(km, start_time, control_distance))

    # Validate inputs
    if km <= 0 or control_distance <= 0:
        return flask.jsonify(error="Distance and control distance must be greater than zero."), 400

    # Calculate open and close times
    open_time = acp_times.open_time(km, control_distance, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, control_distance, start_time).format('YYYY-MM-DDTHH:mm')

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

