import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('clouddirectory', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["development_schemas"] = get_development_schema_arns()
    resources["directories"] = get_directories()
    resources["published_schemas"] = get_published_schema_arns()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources

def get_development_schema_arns():
  fields = []
  return get_service("list_development_schema_arns", "SchemaArns", fields)

def get_directories():
  fields = ["Name", "DirectoryArn", "State"]
  return get_service("list_directories", "Directories", fields)

def get_published_schema_arns():
  fields = []
  return get_service("list_published_schema_arns", "SchemaArns", fields)
