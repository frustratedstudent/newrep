from flask import Flask, url_for, request, render_template, g, redirect
import sqlite3

DATABASE = 'data/database.db'

app = Flask(__name__)


@app.route('/')
def action():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')
	
@app.route('/home', methods=["POST"])
def choice():

    if(request.form['choice']=='add'):
        return redirect(url_for('trip_form'))
    else:
        return redirect(url_for('map_year'))

		
@app.route('/add', methods=["GET"])
def trip_form():
	return render_template('trip_form.html')

@app.route('/add', methods=["POST"])
def add_trip():

	conn = sqlite3.connect('data/database.db')
	
	cur = conn.cursor()
	
	cur.execute('SELECT country, north, east FROM cities WHERE city=?', [request.form['city']])
	
	row = cur.fetchone()
	country = row[0]
	north = row[1]
	east = row[2]
	
	cur.execute('INSERT INTO visits(country, city, year, img_link, comment, north, east) VALUES(?,?,?,?,?,?,?)',
				[country,request.form['city'],request.form['year'],request.form['img_link'],request.form['comment'], north, east])
				
	conn.commit()
	
	conn.close()
				
	return render_template('success.html')
	
@app.route('/map', methods=["GET"])
def map_year():
	return render_template('map_year.html')
	
@app.route('/map', methods=["POST"])
def show_map():

	conn = sqlite3.connect('data/database.db')
	
	cur = conn.cursor()
	
	if(request.form['year']=='9999'):
		cur.execute('SELECT * FROM visits')
	else:
		cur.execute('SELECT * FROM visits WHERE year=?', [request.form['year']])
	
	rows = cur.fetchall();
	
	print(request.form['year'])
	print(rows)
	
	return render_template('index.htm', rows = rows)

	
	
	
	
if __name__ == '__main__':
    app.run()