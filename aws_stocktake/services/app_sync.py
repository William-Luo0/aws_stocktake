import filter_keys
import boto3
from botocore.exceptions import ClientError

def get_service(function, dict_key, fields, extra_options={}):
  return filter_keys.filter_key('appsync', function, dict_key, fields,
      extra_options)

def get_all(remove_empty=False):
  # Return all resources
  resources = {}
  resources["graphql_apis"] = get_graphql()

  if remove_empty:
    resources = dict((key,value) for key,value in resources.items() if value)

  return resources

def get_graphql():
  fields = ["apiId", "name", "arn"]
  return get_service("list_graphql_apis", "graphqlApis", fields)
