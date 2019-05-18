from quart import Quart, request
from objects import *
from config import Development, Production
import os


def register_route(self, url, return_type, **route_specs):
    async def route(**kwargs):
         return create(return_type)

    if "endpoint" not in route_specs:
        route.__name__ = url
    self.add_url_rule(url, view_func=route, **route_specs)


Quart.register_route = register_route


def create_app(import_name, mode=Development):
    app = Quart(import_name)
    app.config.from_object(mode)
    return app


# Set up app
app = create_app(__name__)

Routes = {
    "/v2/subscriptions/credit-balance": CreditBalance,
    "/next_in_queue": {"return_type": Queue, "endpoint": "next_in_queue"},
    "/api/v1/<string:platform>/user/<int:user_id>": User,
    "/api/v1/<string:platform>/subscription_plan": SubscriptionPlan,
    "/v2/subscriptions/credit/credit-actions": {"return_type": CreditResult, "methods": ["POST"]},
    "/credit_bundle": CreditBundle,
    "/credit_transaction": CreditTransaction,
    "/credit_ledger": CreditLedger,
    "/credit_transfer": CreditTransfer,
    "/nested_obj_test": Parent,
}

for route, route_specs in Routes.items():
    if "return_type" in route_specs:
        app.register_route(route, **route_specs)
    else:
        app.register_route(route, route_specs)

app.run()
