import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- TERE API KEYS ---
GNEWS_KEY = '5b8559e3138b18090304c361c25653b0'
MARKETAUX_KEY = 'YSU6oi4R1R0WahkqNdMWRUMyH5OPQSX8NuQ7nL3Y'

@app.route('/')
def index():
    cat = request.args.get('category', 'general')
    articles = []

    try:
        if cat == 'business': # FOREX (MarketAux use karenge)
            url = f"https://api.marketaux.com/v1/news/all?symbols=EURUSD,GBPUSD,JPY&filter_entities=true&language=en&api_token={MARKETAUX_KEY}"
            res = requests.get(url).json()
            for a in res.get('data', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a.get('image_url', 'https://images.unsplash.com/photo-1611974714024-462002ca0c71?w=500'),
                    'publishedAt': a['published_at'][:10]
                })
        
        elif cat == 'technology': # CRYPTO (GNews with Crypto query)
            url = f"https://gnews.io/api/v4/search?q=crypto+bitcoin&lang=hi&country=in&max=10&apikey={GNEWS_KEY}"
            res = requests.get(url).json()
            for a in res.get('articles', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a['image'],
                    'publishedAt': a['publishedAt'][:10]
                })

        elif cat == 'science': # STOCKS (GNews with Nifty/Stocks)
            url = f"https://gnews.io/api/v4/search?q=stock+market+nifty+sensex&lang=hi&country=in&max=10&apikey={GNEWS_KEY}"
            res = requests.get(url).json()
            for a in res.get('articles', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a['image'],
                    'publishedAt': a['publishedAt'][:10]
                })

        else: # GENERAL HINDI NEWS
            url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&max=15&apikey={GNEWS_KEY}"
            res = requests.get(url).json()
            for a in res.get('articles', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'url': a['url'],
                    'urlToImage': a['image'],
                    'publishedAt': a['publishedAt'][:10]
                })
    except Exception as e:
        print(f"Error: {e}")

    return render_template('index.html', articles=articles)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    content = data.get('summary', '')
    summary = f"Analysis: {content[:180]}... Status: Active Monitoring."
    return jsonify({"result": summary})

if __name__ == '__main__':
    app.run(debug=True)

