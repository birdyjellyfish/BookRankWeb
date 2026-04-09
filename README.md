# BookRankWeb
Web interface for BookRank book recommendation engine

## Installation

### Requirements
- Node.js v24.14.0 and above
- Sqlite3 database containing Book information for backend
- igraph file containing BookRank network
- Python 3.14 and above

### Installing dependencies

In the root BookRankWeb folder, install python dependencies
```
pip install -r requirements.txt
```
It is recommended to install the python dependencies in a
python virtual env (like venv)

Next, in the frontend folder, install node packages
```
cd frontend
npm install
```
Place your graph file in ```/backend/api/```
Place your database file in ```/backend/```
Edit the .env file in ```/backend```  

