import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('application-autoscaling', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["scalable_targets"] = get_targets()
    resources["scaling_policies"] = get_policies()
    resources["scheduled_actions"] = get_schedules()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_targets():
    service_namespace = ["ecs", "elasticmapreduce", "ec2", "appstream",
                         "dynamodb", "rds", "sagemaker"]
    fields = ["ServiceNamespace", "ResourceId", "ScalableDimension"]

    targets = []
    for service in service_namespace:
        targets.append(get_service("describe_scalable_targets", "ScalableTargets",
                                   fields, {"ServiceNamespace": service}))

    targets = [x for x in targets if x]
    return targets


def get_policies():
    service_namespace = ["ecs", "elasticmapreduce", "ec2", "appstream",
                         "dynamodb", "rds", "sagemaker"]
    fields = ["ServiceNamespace", "PolicyARN", "PolicyName", "ScalableDimension"]

    targets = []
    for service in service_namespace:
        targets.append(get_service("describe_scaling_policies", "ScalingPolicies",
                                   fields, {"ServiceNamespace": service}))

    targets = [x for x in targets if x]
    return targets


def get_schedules():
    service_namespace = ["ecs", "elasticmapreduce", "ec2", "appstream",
                         "dynamodb", "rds", "sagemaker"]
    fields = ["ServiceNamespace", "ScheduledActionARN", "ScheduledActionName", "ScalableDimension"]

    targets = []
    for service in service_namespace:
        targets.append(get_service("describe_scheduled_actions", "ScheduledActions",
                                   fields, {"ServiceNamespace": service}))

    targets = [x for x in targets if x]
    return targets
