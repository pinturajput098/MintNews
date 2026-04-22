import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🔑 TERA NEWS API KEY (Check kar lena sahi hai ya nahi)
NEWS_API_KEY = '9d1872cc335a494793708453f6560965' # <--- Yahan apni key daal dena

@app.route('/')
def index():
    # Sidebar se aane wali category/section ko pakadna
    category = request.args.get('category', 'top-headlines')
    
    # Section ke hisaab se News filter karna (Trading focus)
    if category == 'business':
        query = 'forex trading market'
    elif category == 'technology':
        query = 'bitcoin crypto blockchain'
    elif category == 'science':
        query = 'stock market nifty trading'
    else:
        query = 'latest news'

    # URL setup (Trading/Finance focus ke liye query base)
    url = f'https://newsapi.org/v2/everything?q={query}&language=hi&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        # Sirf wahi articles rakhna jinka image ho taaki site "khali" na lage
        filtered_articles = [a for a in articles if a.get('urlToImage')]
    except:
        filtered_articles = []

    return render_template('index.html', articles=filtered_articles[:20], current_cat=category)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Jarvis AI Analysis logic
    data = request.json
    content = data.get('summary', 'No data available.')
    
    # AI Summary logic (Chota aur crisp)
    summary = f"📑 Quick Info: {content[:150]}... ✨ Status: 🔥 Hot Topic"
    return jsonify({"result": summary})

if __name__ == '__main__':
    app.run(debug=True)

