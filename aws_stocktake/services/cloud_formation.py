import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('cloudformation', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["stack_sets"] = get_stack_sets()
    resources["stacks"] = get_stacks()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources

def get_stack_sets():
  fields = ["StackSetName", "StackSetId", "Status"]
  return get_service("list_stack_sets", "Summaries", fields)

def get_stacks():
  fields = ["StackId", "StackName", "StackStatus"]
  return get_service("list_stacks", "StackSummaries", fields)

