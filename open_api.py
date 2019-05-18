from yaml import Loader, load
from requests import get

response = get("https://petstore.swagger.io/v2/swagger.yaml")
source = load(response.content, Loader=Loader)

paths = source["paths"]
