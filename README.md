# How To Run:

## Clone the repository
```sh
git clone git@github.com:4ikkamony/log-test-task.git
```

```sh
cd log-test-task
```
## 1. Run using Docker Compose

```sh
cp .env.sample .env
```
[Optional] Place your custom .log file into 'logs' folder
and set its name to ```LOG_FILE_NAME``` variable in ```.env```
By default, it is set to app_2.log

### Run task_1 and task_2
```sh
docker compose up
```

## 2. Run locally

### Create and activate venv
```sh
python -m venv .venv
```

linux:
```sh
source .venv/bin/activate
```

windows:
```sh
.venv\Scripts\activate
```

### Install requirements
```sh
pip install -r requirements.txt
```

## Run Task 1
To run with default app_2.log file:
```sh
python do_it_yourself.py
```
Or specify path to your log file:
```sh
python do_it_yourself.py path/to/file
 ```

## Run Task 2
Run the tests:
```sh
pytest
```
