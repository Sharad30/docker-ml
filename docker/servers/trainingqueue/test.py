import requests

api = "http://127.0.0.1:8000"

dataset_id = "123"
container_id = "1123"
codebase_id = "32"
status = "pending"

response = requests.get(
    f"{api}/create/job/?dataset_id={dataset_id}&container_id={container_id}&codebase_id={codebase_id}&status={status}"
)
print(response.status_code)
print(response)

response = requests.get(f"{api}/list/job/?job_id={2}")
print(response.status_code)
print(response.content)
