import requests
from bs4 import BeautifulSoup


def requests_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    # 在页面中找到所有的书籍条目
    book_entries = soup.find_all('li')

    for book in book_entries:
        try:
            list_num_element = book.find('div', class_='list_num red') or book.find('div', class_='list_num')
            list_num = list_num_element.text.strip() if list_num_element else "No list number available"

            name_element = book.find('div', class_='name')
            book_title = name_element.a['title'] if name_element and name_element.a else "No title available"

            author_elements = book.find_all('div', class_='publisher_info')
            author_name = "No author name available"
            publisher = "No publisher available"
            if author_elements:
                author_name = author_elements[0].a.text.strip() if author_elements[0].a else "No author name available"
                publisher = author_elements[1].a.text.strip() if len(author_elements) > 1 and author_elements[
                    1].a else "No publisher available"

            price_element = book.find('span', class_='price_n')
            price = price_element.text.strip() if price_element else "No price available"

            print("标签号:", list_num)
            print("书名:", book_title)
            print("作者姓名:", author_name)
            print("出版社:", publisher)
            print("价格:", price)
            print("----------------------------")
        except Exception as e:
            print(f"An error occurred while processing a book: {e}")
            continue


def main():
    for page in range(1, 26):  # 从第1页到第25页
        url = f'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-{page}'
        html = requests_dandan(url)
        if html:
            parse_html(html)
        else:
            print(f"Failed to retrieve data from page {page}")


if __name__ == "__main__":
    main()

