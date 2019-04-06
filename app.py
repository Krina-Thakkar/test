from flask import Flask, render_template, request

import app2
app= Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Scraped data
@app.route('/data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        # Get Lyrics
        k = int(request.form['k'])
    scr = app2.scrape(k)
    pred_song = app2.song_classifier(scr)
    print(pred_song)
    return render_template('hello.html',scr=pred_song)
    
if __name__ == '__main__':
    app.run(debug=True)

