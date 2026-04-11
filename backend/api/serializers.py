from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import Books, Genres, BookUser
import requests
from dotenv import load_dotenv
import os
from django.conf import settings
import time

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

API_KEY = os.getenv("NLB_APIKEY")
APP_CODE = os.getenv("NLB_APPCODE")

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ["genreid", "name"]

# NOTE: to serialize a recommendation, e.g. queryset of books
# run BookSerializer(reco, many=True)
class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    isbn = serializers.CharField() # typecast isbn to charfield since there are some isbn with X
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = ["bookid", "goodreadsbookid", "coverid", "isbn", "authors", "title", "averagerating", "weightedscore", "ratingscount", "genres", "availability"]

    def get_availability(self, obj):
        libraries = []
        title = obj.title
        authors = obj.authors
        authors = authors.replace(',', '')

        # clean title by removing brackets and text within
        while '(' in title or ')' in title:
            open_bracket = title.find('(')
            close_bracket = title.find(')')
            title = title[:open_bracket] + title[close_bracket+1:]

        title = title.strip()

        keywords = title.split(' ')
        # append authors names
        keywords += authors.split(' ')

        query = ' '.join(keywords)

        print(query)

        brn = None

        try:
            url = f"https://openweb.nlb.gov.sg/api/v2/Catalogue/SearchTitles?Keywords={query}&MaterialTypes=bks"

            headers = {
                "X-Api-Key": API_KEY,
                "X-App-Code": APP_CODE
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                for book in response.json()['titles']:
                    if title == book['title']:
                        brn = book['records'][0]['brn']
                        break
            
        except:
            brn = None
        
        # check if we got a brn
        if brn is None:
            return []
        time.sleep(2)
        
        # else retrieve availability by brn
        try:
            url = f"https://openweb.nlb.gov.sg/api/v2/Catalogue/GetAvailabilityInfo?BRN={brn}"

            headers = {
                "X-Api-Key": API_KEY,
                "X-App-Code": APP_CODE
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                for item in response.json()['items']:
                    if item['transactionStatus']['code'] == 'S':
                        libraries.append(item['location']['name'])
        except:
            libraries = []
        
        return libraries


# returns bookid, authors, title only
# stripped for BookSearch view and others
class BookLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ["bookid", "coverid", "authors", "title"]


class BookUserSerializer(serializers.ModelSerializer):
    coverid = serializers.IntegerField(source="book.coverid", read_only=True)
    authors = serializers.CharField(source="book.authors", read_only=True)
    title = serializers.CharField(source="book.title", read_only=True)
    
    bookid = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(),
        source="book"
    )

    class Meta:
        model = BookUser
        fields = ["bookid", "coverid", "authors", "title", "datefinished"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# for register
class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    # custom create function otherwise User will not be created properly
    # password not hashed under normal model add() function
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# serializer class to deserialize recommendation request from user
class RecoSerializer(serializers.Serializer):
    genre = serializers.IntegerField(required=False, allow_null=True)
    lastread = serializers.IntegerField()
    n = serializers.IntegerField(default=10)
    k = serializers.IntegerField(default=100)


