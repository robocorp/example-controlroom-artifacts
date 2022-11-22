from urllib.parse import urlparse


def get_address_without_dots(url):
    url_parsed = urlparse(url)
    combination = f"{url_parsed.netloc}{url_parsed.path}"
    return combination.replace(".", "").replace("/", "")


if __name__ == "__main__":
    print(get_address_without_dots("https://github.com/robocorp/rpaframework"))
