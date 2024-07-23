from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        print(url)
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # Extract data with improved selectors and error handling (consider using libraries like Scrapy or Selenium for more complex scraping)
            image_element = soup.find("img", class_="DByuf4 IZexXJ jLEJ7H")
            image_url = image_element.get("src") if image_element else "N/A"

            title_element = soup.find("h1", class_="_6EBuvT")
            title = title_element.text.strip() if title_element else "N/A"

            mrp_element = soup.find("div", class_="yRaY8j A6+E6v")
            mrp = mrp_element.text.strip() if mrp_element else "N/A"

            price_element = soup.find("div", class_="Nx9bqj CxhGGd")
            selling_price = price_element.text.strip() if price_element else "N/A"

            description_element = soup.find("div", class_="yN+eNk w9jEaj")
            description = description_element.text.strip() if description_element else "N/A"

            higlited_list = []
            highlight_element = soup.find("div", class_="xFVion")
            if highlight_element:
                highlights = highlight_element.find("ul")
                if highlights:
                    highlight_list = highlights.findAll("li")
                    if highlight_list:
                        for item in highlight_list:
                            higlited_list.append(item.text)
            
            print(higlited_list)

            rating_element = soup.find("div", class_="XQDdHH")
            rating = rating_element.text.strip() if rating_element else ""

            reviews_element = soup.find("span", class_="Wphh3N")
            reviews = reviews_element.text.strip() if reviews_element else ""

            offers_element = soup.find("div", class_="cPHDOP col-12-12")
            offers = offers_element.text.strip() if offers_element else ""

            data = {
                "image_url": image_url,
                "title": title,
                "mrp": mrp,
                "selling_price": selling_price,
                "description": description,
                "higlited_list": higlited_list,
                "rating": rating,
                "reviews": reviews,
                "offers": offers,
                "more":url
            }
            return render_template('index.html', data=data)
        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred: {e}"
            return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)