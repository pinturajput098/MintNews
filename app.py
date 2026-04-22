import requests
import feedparser # Isse RSS feed fetch hogi
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# GNews for General & Hindi News
GNEWS_KEY = '76110f215d8625a676b772421376378e'

def fetch_rss(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:15]:
        articles.append({
            'title': entry.title,
            'description': entry.get('summary', 'Market Update'),
            'url': entry.link,
            'urlToImage': 'https://images.unsplash.com/photo-1611974714024-462002ca0c71?auto=format&fit=crop&w=500', # Placeholder for trading
            'full_desc': entry.get('summary', '')
        })
    return articles

@app.route('/')
def index():
    cat = request.args.get('category', 'general')
    articles = []

    if cat == 'business': # FOREX
        articles = fetch_rss("https://www.dailyfx.com/feeds/forex-market-news")
    elif cat == 'technology': # CRYPTO
        articles = fetch_rss("https://news.google.com/rss/search?q=crypto+bitcoin&hl=hi&gl=IN&ceid=IN:hi")
    elif cat == 'science': # STOCKS
        articles = fetch_rss("https://news.google.com/rss/search?q=nifty+sensex+stocks&hl=hi&gl=IN&ceid=IN:hi")
    else: # GENERAL HINDI
        url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&max=10&apikey={GNEWS_KEY}"
        res = requests.get(url).json()
        for a in res.get('articles', []):
            articles.append({
                'title': a['title'],
                'description': a['description'],
                'url': a['url'],
                'urlToImage': a['image'],
                'full_desc': a['content']
            })

    return render_template('index.html', articles=articles)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    summary = f"📑 System Insight: {data.get('summary', '')[:150]}... | ⚡ Risk: Analyzed."
    return jsonify({"result": summary})

if __name__ == '__main__':
    app.run(debug=True)

