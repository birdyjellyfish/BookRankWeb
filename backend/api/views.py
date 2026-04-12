from api.models import Books, Genres, BookUser
from api.serializers import BookSerializer, GenreSerializer, RecoSerializer, UserSerializer, BookUserSerializer, UserAuthSerializer, BookLiteSerializer, BookAvailabilitySerializer
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.db.utils import IntegrityError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .bookrank import BookRank
import igraph as ig
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
graph_filename = os.getenv("GRAPH_FILENAME")
graph_format = os.getenv("GRAPH_FORMAT")

print('Loading GRAPH object...')
GRAPH_PATH = os.path.join(settings.BASE_DIR, 'data', graph_filename)
GRAPH = ig.read(GRAPH_PATH, format=graph_format)
print('GRAPH successfully loaded.')

# Create your views here.

@ensure_csrf_cookie
@api_view(["GET"])
def SetCSRFToken(request):
    """Set CSRF Token for frontend"""
    if request.method == "GET":
        return Response({'message': 'CSRF cookie set'}, status=status.HTTP_200_OK)

class BookPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size' # user can set page_size
    max_page_size = 100 # max page_size user can set / will be returned


class BookDetail(generics.RetrieveAPIView):
    """
    Retrieve Book details by bookid
    """
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookAvailability(generics.RetrieveAPIView):
    """
    Retrieve Book availability by its bookid
    Since we are rate limited by NLB, retrieval of BookDetail may take 2s or longer
    Availability may be empty either because book is really not available at NLB,
    or because of rate limit
    """
    queryset = Books.objects.all()
    serializer_class = BookAvailabilitySerializer


class GenreDetail(generics.RetrieveAPIView):
    """
    Retrieve Genre details by its genreid
    """
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class GenreList(generics.ListAPIView):
    """
    Retrieve list of genres
    """
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class GenreBookList(generics.ListAPIView):
    """
    Retrieve list of books related to given genreid
    """
    serializer_class = BookLiteSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        genre_id = self.kwargs.get("pk")
        return Books.objects.filter(bookgenre__genreid=genre_id)


class BookSearch(generics.ListAPIView):
    """
    Retrieve list of books, matching with search parameters given
    based on Books.title and Books.authors
    """
    queryset = Books.objects.all()
    serializer_class = BookLiteSerializer
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["authors", "title"]


class Recommender(APIView):
    """
    Return list of recommended books, based on BookRank.py,
    based on User's reading history, last read book, and genre to read next
    """
    def post(self, request, format=None):
        # deserialize recommendation request
        reco_request = RecoSerializer(data=request.data)

        if not reco_request.is_valid():
            return Response(reco_request.errors, status=status.HTTP_400_BAD_REQUEST)

        # unpack values
        genre = reco_request.data.get('genre') # default = None
        lastread = reco_request.data.get('lastread') # required = True
        n = reco_request.data.get('n') # default = 10
        k = reco_request.data.get('k') # default = 100

        # now get user book list
        if request.user.is_anonymous:
            # AnonymousUser
            history = []
        else:
            history = request.user.books.values_list("bookid", flat=True)
        

        # create BookRank object and get recos
        br = BookRank(GRAPH, history)
        recos_list = br.get_book_recco(last_read_book_id=lastread, genreId=genre, n=n, k=k) # returns list of bookids
        queryset = Books.objects.filter(bookid__in=recos_list)
        

        recos_serializer = BookLiteSerializer(queryset, many=True)
        return Response(recos_serializer.data, status=status.HTTP_200_OK)
    

# Views for user
# List books of user

class BookUserList(generics.ListCreateAPIView):
    """
    Returns a list of books the user has read, and the datefinished for each book.
    Also add entry into user's book list

    request.user must match user (i.e. you can only see what you own)
    """
    serializer_class = BookUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookUser.objects.filter(user=self.request.user)
    

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("This book is already in your list.")
    


# RUD operations for BookUser
class BookUserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, delete entry for user's read list
    request.user must match user (i.e. you can only see what you own)
    """
    serializer_class = BookUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "book_id" # find the bookid in queryset

    # filter for specific user only
    def get_queryset(self):
        return BookUser.objects.filter(user=self.request.user)


# User operations
class UserDetail(generics.RetrieveAPIView):
    """
    Retrieves current user's details

    Must be logged in to access
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminUserList(generics.ListAPIView):
    """
    Returns a list of user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BookPagination


class AdminUserDetail(generics.RetrieveAPIView):
    """
    Retrieves a specific user's details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = BookPagination



# Register/Login/Logout Views
class RegisterView(generics.CreateAPIView):
    """
    Create new user object with username, email, password
    """
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer


class LoginView(APIView):
    """
    Authenticates user credentials and logs in if valid
    """
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # authenticate user
        user = authenticate(request, username=username, password=password)
        
        # login user if valid
        if user:
            login(request, user)
            return Response(
                {"message": "Login successful.", "success": True},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Login unsuccessful.", "success": False},
                status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Log out current user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response("Logout successful.", status=status.HTTP_200_OK)
    

class PasswordResetView(APIView):
    """
    Reset password for given user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        newpassword = request.data.get("password")

        # check if newpassword is supplied
        if not newpassword:
            return Response("New pasword must be supplied.", status=status.HTTP_400_BAD_REQUEST)

        user.set_password(newpassword)
        user.save()

        return Response("Password changed successfully.", status=status.HTTP_204_NO_CONTENT)

        


