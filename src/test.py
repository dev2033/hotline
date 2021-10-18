

def main():
    urls = [
        "qwewqeqwe",
        "qweqweqwe"
    ]
    with open("results/invalid_urls/invalid_urls.txt", "w") as file:
        for url in urls:
            file.write(url + "\n")


if __name__ == '__main__':
    main()