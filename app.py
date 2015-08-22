from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def main():
	return redirect('/index')

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

#Main Process
@app.route('/stock/')
def stock():
	stockcode = request.args.get('stockcode')
	
	if stockcode and stockcode.strip():
		#request data from QuanDL
		baseURL='https://www.quandl.com/api/v1/datasets/WIKI/'
		jsonURL=baseURL + stockcode + '.json'
		jsonRespond = requests.get(jsonURL)
		HTTPstatusCode=jsonRespond.status_code
		
		print '[URL]  ' + jsonURL
		print '[HTTP] ' + str(HTTPstatusCode)
		
		#parse data if HTTP Status is OK
		if HTTPstatusCode==200:
			jheader=(jsonRespond.json())['column_names']
			jdata=(jsonRespond.json())['data']
			stockdata=pd.DataFrame(jdata, columns=jheader)
			stockdata["Date"] = pd.to_datetime(stockdata["Date"])
			print stockdata.head()
			
			#To calculate the positions of the bars
			mids = (stockdata.Open + stockdata.Close)/2
			spans = abs(stockdata.Close-stockdata.Open)
			#To check the up/down of the day to determin the bar color
			inc = stockdata.Close > stockdata.Open
			dec = stockdata.Open > stockdata.Close
			
			w = 12*60*60*1000 # half day in ms

			#Render Chart
			# Create a polynomial line graph
			x = list(range(5, 20))
			fig = figure(title="Chart for " + stockcode, plot_width=1000, x_axis_type="datetime")
			#fig.line(x, [i ** 2 for i in x], line_width=2)
			
			fig.segment(stockdata.Date, stockdata.High, stockdata.Date, stockdata.Low, color="black")
			fig.rect(stockdata.Date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
			fig.rect(stockdata.Date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

			plot_resources = RESOURCES.render(
				js_raw=INLINE.js_raw,
				css_raw=INLINE.css_raw,
				js_files=INLINE.js_files,
				css_files=INLINE.css_files,
			)

			script, div = components(fig, INLINE)			

			html=render_template('stock.html', status={'code':1, 'msg':'OK'}, stock={'code':stockcode}, plot={'script':script, 'div':div, 'resources':plot_resources})
		else:
			html=render_template('stock.html', status={'code':2, 'msg':'Server Error'})
	else:
		html=render_template('stock.html', status={'code':3, 'msg':'No Stockcode Entered'})

	return html 
  
if __name__ == '__main__':
	app.run(debug = True)
