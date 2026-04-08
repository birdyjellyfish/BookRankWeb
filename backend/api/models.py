# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Books(models.Model):
    bookid = models.AutoField(db_column='bookId', primary_key=True)  # Field name made lowercase.
    goodreadsbookid = models.IntegerField(db_column='goodreadsBookId')  # Field name made lowercase.
    isbn = models.IntegerField(null=True)
    authors = models.TextField()
    title = models.TextField()
    averagerating = models.FloatField(db_column='averageRating')  # Field name made lowercase.
    weightedscore = models.FloatField(db_column='weightedScore')  # Field name made lowercase.
    ratingscount = models.IntegerField(db_column='ratingsCount')  # Field name made lowercase.

    coverid = models.IntegerField(null=True) # extension of original Books db

    genres = models.ManyToManyField("Genres", through="BookGenre", related_name="books")
    readby = models.ManyToManyField("auth.User", through="BookUser", related_name="books")

    class Meta:
        db_table = 'books'
        ordering = ['bookid']

    def __repr__(self):
        return f"Books(bookid={self.bookid}, authors='{self.authors}', title='{self.title}')"


class Genres(models.Model):
    genreid = models.AutoField(db_column='genreId', primary_key=True)  # Field name made lowercase.
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'genres'
        ordering = ["genreid"]

    def __repr__(self):
        return f"Genres(genreid={self.genreid}, name='{self.name}')"


class Ratings(models.Model):
    pk = models.CompositePrimaryKey('bookida', 'bookidb')
    bookida = models.IntegerField(db_column='bookIdA')  # Field name made lowercase.
    bookidb = models.IntegerField(db_column='bookIdB')  # Field name made lowercase.
    averagerating = models.FloatField(db_column='averageRating')  # Field name made lowercase.
    sumrating = models.IntegerField(db_column='sumRating')  # Field name made lowercase.
    ratingscount = models.TextField(db_column='ratingsCount')  # Field name made lowercase. This field type is a guess.
    weightedscore = models.FloatField(db_column='weightedScore')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ratings'


class BookGenre(models.Model):
    bookid = models.ForeignKey('Books', models.CASCADE, db_column='bookId')  # Field name made lowercase.
    genreid = models.ForeignKey('Genres', models.CASCADE, db_column='genreId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_genre'


# additional models to keep track of user data - not in original BookRank db
class BookUser(models.Model):
    book = models.ForeignKey('Books', on_delete=models.CASCADE, db_column='bookId')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    datefinished = models.DateField(null=True)

    class Meta:
        db_table = 'book_user'
        ordering = ["user", "book"]
        constraints = [
            models.UniqueConstraint(fields=['book', 'user'], name='bookuser_record')
        ]