from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Design routes
@app.route('/design/digital')
def digital():
    return render_template('design_digital.html')

# ... Additional routes for each subcategory ...

# Art routes
@app.route('/art/audio/music')
def music():
    return render_template('music.html')

# ... And so on for every subcategory ...

# Philosophy routes
@app.route('/philosophy/mission/observations')
def observations():
    return render_template('observations.html')

# ... Continue this pattern ...

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    app.run(debug=True)
