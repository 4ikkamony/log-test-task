# How To Run:

```sh
git clone git@github.com:4ikkamony/log-test-task.git
```

```sh
cd log-test-task
```

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

  ## Task 1:
  To run with default app_2.log file:
  ```sh
  python -m task_1.do_it_yourself
  ```
  Or specify path to your log file:
  ```sh
  python -m task_1.do_it_yourself path/to/file.log
   ```

  ## Task 2:
  Run the tests:
  ```sh
  pytest
  ```
