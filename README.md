# How To Run:

#### Clone the project
```sh
git clone git@github.com:4ikkamony/log-test-task.git
```

```sh
cd log-test-task
```
## Now you have 2 options

### 1. Run with Docker Compose:

#### [Optional] Use custom log file:
```sh
cp .env.sample .env
```
By default, logs/app_2.log file is used.
To use other file, put it in 'logs' folder, and specify its name in .env file
```sh
LOG_FILE_NAME=app_2.log
```

```sh
docker compose up
```

### 2. Run locally:

#### Create and activate venv
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

#### Install requirements
```sh
pip install -r requirements.txt
```

  #### Task 1:
  To run with default app_2.log file:
  ```sh
  python -m task_1.do_it_yourself
  ```
  Or specify path to your log file:
  ```sh
  python -m task_1.do_it_yourself path/to/file.log
   ```

  #### Task 2:
  Run the tests:
  ```sh
  pytest
  ```
