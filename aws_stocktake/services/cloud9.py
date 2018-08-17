import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('cloud9', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["environments"] = get_environments()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_environments():
    fields = []
    return get_service("list_environments", "environmentIds", fields)
