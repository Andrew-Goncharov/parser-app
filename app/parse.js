const container = document.querySelectorAll('[itemprop="image"]');

for (let i = 0; i < container.length; i++) {
    img = container[i].querySelector('img').src;
    console.log(img);
}