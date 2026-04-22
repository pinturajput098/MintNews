import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- TERI SABHI KEYS ---
NEWSDATA_API_KEY = 'pub_f0d2885fbc0141a3ac716a0aa60f2f5e'

@app.route('/')
def index():
    cat = request.args.get('category', 'top')
    url = f'https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&country=in&language=hi,en&category={cat}'
    
    try:
        r = requests.get(url, timeout=10).json()
        articles = []
        if r.get('status') == 'success':
            for a in r.get('results', []):
                desc = a.get('description') or a.get('title')
                clean_summary = desc[:150] + "..." if len(desc) > 150 else desc
                
                articles.append({
                    'title': a.get('title'),
                    'full_desc': clean_summary,
                    'url': a.get('link'),
                    'urlToImage': a.get('image_url') or 'https://via.placeholder.com/400x200?text=Mint+News'
                })
        return render_template('index.html', articles=articles, current_cat=cat)
    except:
        return render_template('index.html', articles=[], current_cat=cat)

@app.route('/analyze', methods=['POST'])
def analyze():
    summary_text = request.json.get('summary', '')
    moods = ["✅ Positive News", "📢 Trending", "🔥 Hot Topic", "🔍 Informative"]
    import random
    return jsonify({
        'result': f"📝 Quick Info: {summary_text} \n\n✨ Status: {random.choice(moods)}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

