import asyncio
from django.conf import settings
import math
from library.models import Book, Author
import requests


def add_books_to_model(num_of_books, title):
    list_books = []
    num_of_calls = math.ceil(num_of_books / 32)

    url = settings.URL_TO_GET_LIST_OF_BOOKS
    for i in range(1, num_of_calls + 1):
        params = {"page": i, "amp:search": title}
        r = requests.get(url=url, params=params)
        list_books += r.json()["results"]

    list_books = list_books[:num_of_books]
    for i in list_books:
        book, _ = Book.objects.get_or_create(
            title=i["title"],
            subject=i["subjects"],
            bookshelves=i["bookshelves"],
            book_number=i["id"],
        )
        for j in i["authors"]:
            author, _ = Author.objects.get_or_create(
                name=j["name"], birth_year=j["birth_year"], death_year=j["death_year"]
            )
            book.authors.add(author)
        book.save()
    print("Task Completed")


def get_book_serialized_data(books):
    serialized_data = []
    for book in books:

        serialized_book = {
            "id": book.id,
            "title": book.title,
            "book_number": book.book_number,
            "author": ", ".join([i["name"] for i in list(book.authors.values("name"))]),
            "bookshelves": ", ".join(book.bookshelves.strip("[]").split(", ")),
            "subjects": ", ".join(book.subject.strip("[]").split(", ")),
        }
        serialized_data.append(serialized_book)
    return serialized_data
