from flask import Flask, render_template, request, redirect, url_for

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
	
@app.route('/stock/<stockcode>')
def stock(stockcode):
	return render_template('stock.html', stockcode=stockcode)
  
if __name__ == '__main__':
	app.run(debug = True)
