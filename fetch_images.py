import requests
import json

asteroids = [
    "433 Eros", "101955 Bennu", "4 Vesta", "243 Ida",
    "25143 Itokawa", "Ryugu", "16 Psyche", "2001 FO32",
    "Apophis", "Didymos"
]

output = []

def get_nasa_image(query):
    url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("collection", {}).get("items", [])
        if not items:
            return None
        # Try to get the first thumbnail
        links = items[0].get("links", [])
        for link in links:
            if link.get("rel") == "preview" or link.get("render") == "image":
                return link.get("href")
        # fallback
        return links[0]["href"] if links else None
    except Exception as e:
        print(f"❌ Error for {query}: {e}")
        return None

for name in asteroids:
    print(f"🔍 Searching for: {name}")
    img_url = get_nasa_image(name)
    if img_url:
        output.append({
            "name": name,
            "hazardous": "Apophis" in name or "Bennu" in name,
            "img_url": img_url
        })
        print(f"✅ Found image: {img_url}")
    else:
        print(f"❌ No image found for: {name}")

# Save the results
with open("asteroids.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n✅ Saved to asteroids.json")
