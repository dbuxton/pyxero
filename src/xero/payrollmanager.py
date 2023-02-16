import requests

from .basemanager import BaseManager
from .constants import XERO_PAYROLL_URL
from .utils import singular


class PayrollManager(BaseManager):
    def __init__(self, name, credentials, unit_price_4dps=False, user_agent=None):
        from xero import __version__ as VERSION

        self.credentials = credentials
        self.name = name
        self.base_url = credentials.base_url + XERO_PAYROLL_URL
        self.extra_params = {"unitdp": 4} if unit_price_4dps else {}
        self.singular = singular(name)

        if user_agent is None:
            self.user_agent = (
                "pyxero/%s " % VERSION + requests.utils.default_user_agent()
            )
        else:
            self.user_agent = user_agent

        for method_name in self.DECORATED_METHODS:
            method = getattr(self, "_%s" % method_name)
            setattr(self, method_name, self._get_data(method))

    def _parse_api_response(self, response, resource_name):
        data = json.loads(response.text, object_hook=json_load_object_hook)
        assert data["httpStatusCode"] == "OK", (
            "Expected the API to say OK but received %s" % data["Status"]
        )

        try:
            return data[resource_name]
        except KeyError:
            return data
