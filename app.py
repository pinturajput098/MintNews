import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
NEWS_API_KEY = '9d1872cc335a494793708453f6560965'

@app.route('/')
def index():
    query = request.args.get('category', 'india news')
    # NewsAPI Everything focus for flexibility
    url = f'https://newsapi.org/v2/everything?q={query}&language=hi&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    
    try:
        r = requests.get(url).json()
        articles = r.get('articles', [])[:20]
    except:
        articles = []
    
    return render_template('index.html', articles=articles)

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.json.get('summary', '')
    summary = f"Summary: {content[:150]}... System Status: All clear."
    return jsonify({"result": summary})

if __name__ == '__main__':
    app.run(debug=True)

