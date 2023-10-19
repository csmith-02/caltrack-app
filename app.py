from flask import Flask, redirect, render_template

app = Flask(__name__)

# Routes

@app.get('/today')
def index():
    return render_template('today.html', heading='TODAY')

@app.post('/today')
def post_calories():
    return redirect('/today', 302)

@app.get('/settings')
def settings():
    return render_template('settings.html', heading='SETTINGS')

@app.get('/track')
def track():
    return render_template('track.html',heading='TRACK')

# keep this condition at the bottom of the file
if __name__ == "__main__":
    app.run(debug=True)
