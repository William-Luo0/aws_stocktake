import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('autoscaling-plans', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["scaling_plans"] = get_scaling_plans()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources

def get_scaling_plans():
  fields = ["ScalingPlanName", "ScalingPlanVersion", "StatusCode"]
  return get_service("describe_scaling_plans", "ScalingPlans", fields)