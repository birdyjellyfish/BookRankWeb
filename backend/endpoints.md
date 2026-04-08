API Endpoints:

Domain: bookrank.com (for example)

API root: /api/

#### /api/recommender
- [x] POST: genreid to filter, last read book
- return json list of books to reccommend, based on user's reading history
- reading history can be queried from inside the function, based on user id


#### /api/book/<int:pk> - return details of books
- [x] GET: bookid -> retrieve exact bookid


#### /api/book/?search=...
- [x] POST: title -> retrieve list of books with matching title / author (for search)


#### api/genre/ - return details of genres
- [x] GET -> retrieve list of genres


#### /api/genre/<int:pk>
- [x] GET -> retrieve genre details


#### /api/readlist/ - return user's reading history
- only owner of the account can see and do CRUD actions
- IsAuthenticated - only those authenticated can see
- [x] **/api/readlist/** GET -> get User's reading history
- [x] **/api/readlist/** POST: bookid, datefinished -> add new book to reading history
- [x] **/api/readlist/<int:book_id>/** GET -> retrieve book details and datefinished from reading history
- [x] **/api/readlist/<int:book_id>/** PATCH: userid, bookid, datefinished -> update book details
- [x] **/api/readlist/<int:book_id>/** DELETE: userid, bookid -> delete book from reading history


#### /api/users/ - return user info / register / login / logout
- IsAuthenticated
- [x] **/api/users/** GET -> get user info for current user
- [x] **/api/users/all** GET -> get user info for all users (IsAdminUser)
- [x] **/api/users/<int:pk>** GET -> get user info for specific user (IsAdminUser)

- [x] **/api/users/register** POST: username, password, email -> create user account
- [x] **/api/users/login** POST: username, password
- [x] **/api/users/logout** POST (IsAuthenticated)
- [x] **/api/users/passwordreset** POST: password -> reset password (IsAuthenticated)