import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GNEWS_KEY = '5b8559e3138b18090304c361c25653b0'
MARKETAUX_KEY = 'YSU6oi4R1R0WahkqNdMWRUMyH5OPQSX8NuQ7nL3Y'

@app.route('/')
def index():
    cat = request.args.get('category', 'india')
    articles = []
    try:
        if cat == 'business': # FOREX SECTION
            url = f"https://api.marketaux.com/v1/news/all?symbols=EURUSD,GBPUSD,JPY&filter_entities=true&language=en&api_token={MARKETAUX_KEY}"
            res = requests.get(url).json()
            for a in res.get('data', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a.get('image_url', 'https://images.unsplash.com/photo-1611974714024-462002ca0c71?w=500'),
                    'publishedAt': a['published_at'][:10],
                    'type': 'forex' # Hardcoded for Bybit
                })
        else: # CRYPTO & OTHERS
            query = "crypto bitcoin" if cat == 'technology' else ("stock market nifty" if cat == 'science' else "india news")
            url = f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&max=12&apikey={GNEWS_KEY}"
            res = requests.get(url).json()
            for a in res.get('articles', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a['image'],
                    'publishedAt': a['publishedAt'][:10],
                    'type': 'crypto' if cat == 'technology' else 'general'
                })
    except: pass
    return render_template('index.html', articles=articles)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    summary = f"MINT AI ANALYSIS: {data.get('summary', '')[:140]}... System Status: Optimized."
    return jsonify({"result": summary})

if __name__ == '__main__':
    app.run(debug=True)

