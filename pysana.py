try:
    import api_key
except ImportError:
    pass

import api


data = api.json_request("users/me")
user = api.User(data["data"])
user.map_attributes(data["data"])
for workspace in user.workspaces:
    print workspace.name, workspace.is_organization
