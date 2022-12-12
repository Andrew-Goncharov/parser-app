import requests
from bs4 import BeautifulSoup as bs


def get_parsed_data(save_data: bool = False) -> list[str]:
    URL = "https://unsplash.com/t/architecture-interior"
    r = requests.get(URL)

    data = bs(r.text, "html.parser")

    if save_data:
        with open("page.html", "w") as file:
            file.write(r.text)

    images = []
    container = data.findAll("figure", itemprop="image")

    for figure in container:
        if figure["data-test"] == "photo-grid-multi-col-figure":
            img = figure.findAll("img")[0]["src"]
            if img not in images:
                images.append(img)

    print(f"Number of images: {len(images)}")

    return images


if __name__ == "__main__":
    get_parsed_data(save_data=True)
