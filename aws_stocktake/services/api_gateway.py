import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('apigateway', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["accounts"] = get_accounts()
    resources["api_keys"] = get_api_keys()
    resources["certificates"] = get_certificates()
    resources["domains"] = get_domains()
    resources["rest_apis"] = get_apis()
    resources["usage_plans"] = get_usages()
    resources["vpc_links"] = get_vpc_links()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_accounts():
    fields = ["cloudwatchRoleArn"]
    return get_service("get_account", "", fields)


def get_api_keys():
    fields = ["id", "name", "description"]
    return get_service("get_api_keys", "items", fields)


def get_certificates():
    fields = ["clientCertificateId", "pemEncodedCertificate", "description"]
    return get_service("get_client_certificates", "items", fields)


def get_domains():
    fields = ["domainName", "certificateArn"]
    return get_service("get_domain_names", "items", fields)


def get_apis():
    fields = ["id", "name", "description", "version"]
    return get_service("get_rest_apis", "items", fields)


def get_usages():
    fields = ["id", "name", "description", "quota"]
    return get_service("get_usage_plans", "items", fields)


def get_vpc_links():
    fields = ["id", "name", "description", "status"]
    return get_service("get_vpc_links", "items", fields)
