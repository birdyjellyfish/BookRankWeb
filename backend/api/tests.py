from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Books, Genres, BookGenre, BookUser
from django.contrib.auth.models import User

# Create your tests here.

# the tests below are for database populated with goodbooks-10k(-enriched)

class BooksTest(APITestCase):
    def setUp(self):
        # fake objects
        Books.objects.create(
            goodreadsbookid=1,
            authors="J.K. Rowling",
            title="Harry Potter",
            averagerating=0,
            weightedscore=0,
            ratingscount=0
        )
        Books.objects.create(
            goodreadsbookid=2,
            authors="C.S. Lewis",
            title="Mere Christianity",
            averagerating=0,
            weightedscore=0,
            ratingscount=0
        )


    def test_get_valid_book(self):
        """
        Test for retrieval of a valid bookid from database
        and return valid data
        """
        url = reverse("book-detail", args=[1]) # trying to find bookid 4
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("bookid"), Books.objects.get(bookid=1).bookid)

    def test_get_invalid_book(self):
        """
        Test for invalid bookid from database
        """
        url = reverse("book-detail", args=[10001])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_booklist(self):
        """
        Test for booklist from database
        """
        url = reverse("book-search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), len(Books.objects.all())) # test number of books

    def test_search_present_book(self):
        """
        Test for searching for present book/author from database
        """
        url = reverse("book-search")
        data = {"search": "C.S. Lewis"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), len(Books.objects.filter(authors="C.S. Lewis")))

    def test_search_absent_book(self):
        """
        Test for searching book/author not in database
        """
        url = reverse("book-search")
        data = {"search": "Final Fantasy 7"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)


class GenresTest(APITestCase):
    def setUp(self):
        Genres.objects.create(name="fiction")
        Genres.objects.create(name="horror")
        Genres.objects.create(name="fantasy")

    def test_get_genrelist(self):
        """
        Test for genrelist from database
        """
        url = reverse("genre-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Genres.objects.all())) # test number of genres

    def test_get_valid_genre(self):
        """
        Test for valid genreid from database
        """
        url = reverse("genre-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), Genres.objects.get(genreid=1).name)

    def test_get_invalid_genre(self):
        """
        Test for invalid genreid from database
        """
        url = reverse("genre-detail", args=[40])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookGenreTest(APITestCase):
    def setUp(self):
        # create genres first
        genre = Genres.objects.create(name="fiction") #id: 1

        # create the books
        book1 = Books.objects.create(
            goodreadsbookid=1,
            authors="J.K. Rowling",
            title="Harry Potter",
            averagerating=0,
            weightedscore=0,
            ratingscount=0
        )

        book2= Books.objects.create(
            goodreadsbookid=1,
            authors="Ray Bradbury",
            title="Fahrenheit 451",
            averagerating=0,
            weightedscore=0,
            ratingscount=0
        )

        book3 = Books.objects.create(
            goodreadsbookid=1,
            authors="Animal Farm",
            title="George Orwell",
            averagerating=0,
            weightedscore=0,
            ratingscount=0
        )

        # now link the books and genres
        BookGenre.objects.create(bookid=book1, genreid=genre)
        BookGenre.objects.create(bookid=book2, genreid=genre)
        BookGenre.objects.create(bookid=book3, genreid=genre)

    def test_get_valid_bookgenrelist(self):
        """
        Test for retrieving books for genreid present in genre list
        """
        url = reverse("genre-book-list", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), len(BookGenre.objects.filter(genreid=1)))

    def test_get_invalid_bookgenrelist(self):
        """
        Test for books for retrieving books for genreid absent from genre list
        """
        url = reverse("genre-book-list", args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), len(BookGenre.objects.filter(genreid=2)))




