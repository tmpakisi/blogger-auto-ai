import time
import random
import requests
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# === CONFIG ===

DEEPSEEK_API_KEY = "sk-2afff136eb77438cb42399dc99287ee4"
PEXELS_API_KEY = "VvyDilkFH2VFvHWHPLY94BRJ9cZDcS2iTRXGlOcb8OK1XmJWEmEZczgZ"
BLOG_ID = "648239613645416316"

# === GOOGLE BLOGGER AUTH ===

creds = Credentials.from_authorized_user_file("credentials.json", ["[https://www.googleapis.com/auth/blogger](https://www.googleapis.com/auth/blogger)"])
service = build("blogger", "v3", credentials=creds)

# === BLOG CATEGORIES ===

CATEGORIES = ["Technology", "Sports", "Finance", "Entertainment", "Politics", "Health", "Lifestyle", "Travel", "Food", "Science"]

def get_trending_topics():
url = "[https://trends.google.com/trends/hottrends/visualize/internal/data](https://trends.google.com/trends/hottrends/visualize/internal/data)"
response = requests.get(url)
if response.status_code == 200:
data = response.json()
return random.choice(data.get("united_states", []))[:10]
return ["AI", "Economy", "Climate Change"]

def get_image(topic):
headers = {"Authorization": PEXELS_API_KEY}
res = requests.get(f"[https://api.pexels.com/v1/search?query={topic}&per_page=1](https://api.pexels.com/v1/search?query={topic}&per_page=1)", headers=headers)
if res.status_code == 200 and res.json().get("photos"):
return res.json()["photos"][0]["src"]["medium"]
return None

def generate_article(topic, category):
prompt = f"Write a 2000-word, SEO-optimized blog post on '{topic}' in the {category} category. Include an introduction, subheadings, and conclusion."
response = requests.post(
"[https://api.deepseek.com/v1/chat/completions](https://api.deepseek.com/v1/chat/completions)",
headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
)
return response.json()["choices"][0]["message"]["content"]

def post_to_blogger(title, content, image_url, category):
full_html = f"<h2>{title}</h2><img src='{image_url}'><p>{content}</p>"
body = {"kind": "blogger#post", "blog": {"id": BLOG_ID}, "title": title, "content": full_html, "labels": [category]}
service.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
print(f"✅ Posted: {title}")

def main():
while True:
print(f"⏰ Running at {datetime.now()}...")
topics = get_trending_topics()
for topic in topics:
category = random.choice(CATEGORIES)
print(f"🧠 Generating post for: {topic} ({category})")
image = get_image(topic)
article = generate_article(topic, category)
post_to_blogger(topic, article, image, category)
time.sleep(300)  # 5 mins between posts
print("Sleeping 3 hours...")
time.sleep(10800)  # 3 hours

if **name** == "**main**":
main()
