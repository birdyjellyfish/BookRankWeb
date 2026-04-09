# BookRankWeb
Web interface for [BookRank](https://github.com/birdyjellyfish/BookRank) book recommendation engine. Made with Vue 3, Tailwind CSS, Shadcn-vue and Django REST Framework.

## Installation

### Requirements
- Node.js v24.14.0 and above
- Sqlite3 database containing Book information for backend (can be generate using [BookRank/data.ipynb](https://github.com/birdyjellyfish/BookRank/blob/main/data.ipynb))
- igraph file containing BookRank network (can be generated using BookRank [BookRank/data.ipynb](https://github.com/birdyjellyfish/BookRank/blob/main/data.ipynb))
- Python 3.14 and above

### Installing dependencies

In the root ```BookRankWeb``` folder, install python dependencies (recommended to activate venv)
```
..\BookRankWeb> pip install -r requirements.txt
```

Next, in the ```frontend``` folder, install node packages
```
..\BookRankWeb\frontend> npm install
```

### Setting up the database
Place your graph and database file in ```/backend/data/```

Edit the .env file in ```/backend/```.
You can also edit the .env file in ```/frontend/``` (if you want to run django from non-default port 8000)

Next, setup the database with django requirements (like User tables etc.)
```
..\BookRankWeb\backend> python manage.py migrate
```

Then, extend the database with coverids from Open Library Covers API in order to display book covers.

Look at ```/backend/db_extension.ipynb``` for example code.

```/backend/db_schema.md``` is the recommended database schema

```/backend/endpoints.md``` specifies each API endpoint

### Usage
This project uses 2 different servers simultaneously, one for the frontend and one for the backend.
```
..\BookRankWeb\backend> python manage.py runserver
```
In another terminal window
```
..\BookRankWeb\frontend> npm run dev
```
Interface with the webapp at the link specified in ```\backend\.env```
(by default [http://localhost:5173/](http://localhost:5173))

**Note: It takes a while to load the graph file. Wait for the django server to start up before using the website.



