from flask import Flask, render_template;
from scraper.web_api_scraper import WebAPIScraper;

app = Flask(__name__);

# Renders the home page
@app.route("/")
def home():
  return render_template("index.html");

if __name__ == "__main__":

  test_url = "https://pokeapi.co/?ref=public_apis";
  APIScraper = WebAPIScraper(test_url);
  APIScraper.scrape();
  app.run(debug=True);