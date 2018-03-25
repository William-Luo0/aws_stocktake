import filter_keys
import boto3
from botocore.exceptions import ClientError

def get_service(function, dict_key, fields, extra_options={}):
  return filter_keys.filter_key('athena', function, dict_key, fields,
      extra_options)

def get_all(remove_empty=False):
  # Return all resources
  resources = {}
  resources["named_queries"] = get_named_queries()
  resources["query_executions"] = get_query_executions()

  if remove_empty:
    resources = dict((key,value) for key,value in resources.items() if value)

  return resources

def get_named_queries():
  fields = []
  return get_service("list_named_queries", "NamedQueryIds", fields)

def get_query_executions():
  fields = []
  return get_service("list_query_executions", "QueryExecutionIds", fields)
