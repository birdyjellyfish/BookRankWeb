### Database
#### books
- bookId (INTEGER; PRIMARY KEY)
- goodreadsBookId (INTEGER)
- coverid (INTEGER)
- isbn (INTEGER)
- authors (TEXT)
- title (TEXT)
- ratingsCount (INTEGER)
- averageRating (REAL)
- weightedScore (REAL)

#### ratings
- bookIdA (INTEGER; PRIMARY KEY)
- bookIdB (INTEGER; PRIMARY KEY)
- averageRating (given by users who read B who also read A; A -> B) (REAL)
- sumRating (INTEGER)
- ratingsCount (number of users who read A and B) (INTEGER)
- weightedScore (REAL)

#### book_genre (many - many relationship)
- bookId (INTEGER; FOREIGN KEY)
- genreId (INTEGER; FOREIGN KEY)

#### genres
- genreId (INTEGER; PRIMARY KEY)
- name (TEXT)

#### users
- built-in django model

#### user_book (many - many relationship)
- bookId (INTEGER; FOREIGN KEY)
- userId (django.auth.User)
- dateFinished (DateField)