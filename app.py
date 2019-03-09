from quart import Quart, request
from objects import *
from config import Development, Production
import os

DEPLOYMENT_MODE = Development

def register_route(self, url, return_type, **route_specs):
    async def route(**kwargs):
         return create_obj_from_definition(return_type)

    if "endpoint" not in route_specs:
        route.__name__ = url
        self.deregister_route_if_exists(url)
    else:
        self.deregister_route_if_exists(route_specs["endpoint"])

    self.add_url_rule(url, view_func=route, **route_specs)

def deregister_route_if_exists(self, route):
    if route in self.url_map.endpoints.keys():
        del self.url_map.endpoints[route]
        del self.view_functions[route]

Quart.register_route = register_route
Quart.deregister_route_if_exists = deregister_route_if_exists

def create_app(import_name, mode=DEPLOYMENT_MODE):
    app = Quart(import_name)
    app.config.from_object(mode)
    return app

# Set up app
app = create_app(__name__)

# Web pages route
@app.route("/")
def index():
    app.register_route("/x", User)
    return "Welcome"


# API Routes
Routes = {
    "/next_in_queue": {"return_type": Queue, "endpoint": "next_in_queue"},
    "/api/v1/<string:platform>/user/<int:user_id>": User,
    "/api/v1/<string:platform>/subscription_plan": SubscriptionPlan,
    "/nested_obj_test": Parent,
}

for route, route_specs in Routes.items():
    if "return_type" in route_specs:
        app.register_route(route, **route_specs)
    else:
        app.register_route(route, route_specs)

app.run(port=DEPLOYMENT_MODE.PORT)
