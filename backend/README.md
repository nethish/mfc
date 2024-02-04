# Get started
## Install dependencies
* Python version 3.9 is used for this project. You can use pyenv to manage python versions
* The dependencies are managed by poetry. Run poetry install to install the dependencies
```bash
poetry install
```

## Database
* Sqlite3 is used to store basic data.
* The database is inside database directory -- mf.db

## Start the server
* The source code goes into backend directory
* To start the server, run below command within backend directory
```bash
uvicorn main:app --reload
```
* poetry manages the dependecies and virtual environment itself. To activate the virtual environment explicitly, run
```bash
poetry shell
```

## APIs
* /api/v1/parse_cas_summary
