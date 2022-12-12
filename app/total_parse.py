import requests
import json


def get_parsed_data(count_pages: int = 10) -> list[str]:
    img_urls = []

    for i in range(count_pages):
        source_url = f"https://unsplash.com/napi/topics/architecture-interior/photos?page={i}&per_page=100"
        r = requests.get(source_url)

        data = json.loads(r.text)

        for j in range(len(data)):
            img_url = data[j]["urls"]["raw"]

            if img_url not in img_urls:
                img_urls.append(img_url)

    print(f"Number of parsed images: {len(img_urls)}")

    return img_urls


if __name__ == "__main__":
    get_parsed_data(count_pages=100)
