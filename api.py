import requests
from urlparse import urljoin
from asyncmodel import AsyncModel

"""
    Python API client for Asana to-dos
"""


class User(AsyncModel):
    """
        Users have 4 fields:
            email -- string
            name -- string
            photo -- map of the user's avatar in various sizes,
                     or null if no avatar is set
            workspaces -- Workspaces and organizations this user may access
                          [ { id: 14916, name: "My Workspace"} ... ]
    """
    def loader_for_attribute(self, name):
        if name in ("email", "name", "photo"):
            #Return the value passed in
            return lambda x: x

        if name == "workspaces":
            return Workspace


class Workspace(object):
    """
        Workspaces have 2 fields:
        name -- string
        is_organization -- boolean
        email_domains -- list of some nature
    """
    def __init__(self, wid):
        self.id = wid["id"]
        data = get_workspace(self.id)
        self.name = data["name"]
        self.email_domains = data["email_domains"]
        self.is_organization = data["is_organization"]


class APIException(Exception):
    pass


api_key = ''


def set_key(key):
    global api_key
    api_key = key


def json_request(endpoint, method="GET", data=None):
    method = method.upper()

    if method in ("POST", "PUT") and data is None:
        raise APIException("HTTP Method %s expects args; none provided."
                           % method)

    url = urljoin("https://app.asana.com/api/1.0/", endpoint)
    return requests.request(method, url,
                            auth=(api_key, ''), data=data).json()


def get_workspace(wid):
    response = json_request("workspaces/%d" % wid)
    return response["data"]
