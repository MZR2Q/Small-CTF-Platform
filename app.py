from flask import Flask, render_template, request, session, redirect,make_response
import sqlite3,html
from datetime import datetime

app = Flask(__name__)
app.secret_key = '88888888888888888888'


def store_flag_submission(sname, sid, flag, points):
    connection = sqlite3.connect('flaghis.db')
    cursor = connection.cursor()

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO flaghistory (sname, sid, flag, date, point)
        VALUES (?, ?, ?, ?, ?)
    ''', (sname, sid, flag, date_str, points))

    connection.commit()
    connection.close()

flags_and_points = {
    'UHBFlag{Z_HTML_VERY_IMPORT_?_Z}': 10.99,
    'UHBFlag{__CSS_FOR__COLOR_MORE_?????}':10.78,
    'UHBFlag{?_JS_IMPORT_?_FOX_?}': 20.99,
    'UHBFlag{?__js_IMPORT_?_?_?__}': 30.55,
    'UHBFlag{Payload_?__}':40.35,
    'UHBFlag{?__Console?_WH_}':40.8,
    'UHBFlag{_CoCKIs_I_?_?_}':40.66,
}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        session['Name'] = html.escape(request.form.get('name'))
        session['id'] = html.escape(request.form.get('id'))
        return redirect('/flagsub')

    return render_template('login.html')


@app.route('/flagsub', methods=['POST', 'GET'])
def flag_submission():

    connection = sqlite3.connect('flaghis.db')
    cursor = connection.cursor()
    cursor.execute('SELECT flag, date, point FROM flaghistory WHERE sname = ? AND sid = ?', (session.get('Name'), session.get('id')))
    flag_history = cursor.fetchall()

    total_points = sum(entry[2] for entry in flag_history)  
    
    if request.method == 'POST':
        flagg = html.escape(request.form.get('flag'))
        flag = str(flagg).replace(' ','')
        if flag in flags_and_points:
            points = flags_and_points[flag]

            cursor.execute('SELECT flag FROM flaghistory WHERE sname = ? AND sid = ? AND flag = ?', (session.get('Name'), session.get('id'), flag))
            existing_flag = cursor.fetchone()

            if existing_flag:
                return redirect('/flagsub')

            store_flag_submission(session.get('Name'), session.get('id'), flag, points)

            return redirect('/flagsub')

    connection.close()

    return render_template('index.html', name=session.get('Name'), id=session.get('id'), flag_history=flag_history, total_points=total_points)




@app.route('/start', methods=['POST', 'GET'])
def sss():


    # Your flag value
    flag_value = 'UHBFlag{_CoCKIs_I_?_?_}'

    # Create a response object
    response = make_response(render_template('zz.html'))

    # Set the cookie
    response.set_cookie('flag_cookie', flag_value)
    return response


def get_top_winners():
    connection = sqlite3.connect('flaghis.db')
    cursor = connection.cursor()

    # Fetch the top 10 winners based on total points
    cursor.execute('''
        SELECT sname, SUM(point) as total_points
        FROM flaghistory
        GROUP BY sname
        ORDER BY total_points DESC
        LIMIT 10
    ''')

    top_winners = cursor.fetchall()

    connection.close()

    return top_winners
@app.route('/dashboard')
def dashboard():
    # Fetch data for the dashboard from the database
    top_winners = get_top_winners()

    return render_template('dashboard.html', top_winners=top_winners)





    return response
if __name__ == '__main__':
    app.run(debug=True)