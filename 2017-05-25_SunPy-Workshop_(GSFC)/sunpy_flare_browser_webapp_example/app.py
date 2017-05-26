from flask import Flask, render_template, Markup
import flask
app = Flask(__name__)
from datetime import datetime, timedelta

from sunpy.net import hek
from sunpy.time import TimeRange
client = hek.HEKClient()

DEFAULT_DAY = datetime.strftime(datetime(2016,1,1), '%Y-%m-%d')
@app.route('/')
def index():
    args = flask.request.args
    this_date = datetime.strptime(args.get('this_date', DEFAULT_DAY), '%Y-%m-%d')

    # query only from NOAA Space Weather Prediction Center (SWPC)
    result = client.query(hek.attrs.Time(this_date, this_date + timedelta(days=1)),
                          hek.attrs.EventType('FL'),
                          hek.attrs.FRM.Name == 'SWPC')

    for res in result:
        res['event_starttime'] = res['event_starttime'][-8:]
        res['event_endtime'] = res['event_endtime'][-8:]

    if 'next_day' in args:
        this_date = this_date + timedelta(days=1)

    if 'prev_day' in args:
        this_date = this_date - timedelta(days=1)

    return render_template('index.html', this_date=datetime.strftime(this_date, '%Y-%m-%d'), data=result)

if __name__ == "__main__":
    print(__doc__)
    app.run(debug=True)
