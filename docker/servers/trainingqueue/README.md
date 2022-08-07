# training-server

Main server:

```python
poetry run uvicorn training_server.main:app --reload
```

Client server:

```python
poetry run uvicorn training_server.client:app --reload
```

```
npm start
    Starts the development server.

npm run build
    Bundles the app into static files for production.

npm test
    Starts the test runner.
````