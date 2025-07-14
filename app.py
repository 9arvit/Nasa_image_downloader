from flask import Flask, render_template, request
import requests
inport os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            items = data.get("collection", {}).get("items", [])[:8]
            for item in items:
                title = item.get("data", [{}])[0].get("title", "Untitled")
                img_url = item.get("links", [{}])[0].get("href", "")
                results.append({
                    "name": title,
                    "img_url": img_url
                })
        except Exception as e:
            print(f"Error: {e}")
    return render_template("asteroid.html", results=results, query=query)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
