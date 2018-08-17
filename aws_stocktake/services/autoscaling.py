import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('autoscaling', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["autoscaling_groups"] = get_autoscaling_group()
    resources["autoscaling_instances"] = get_autoscaling_instances()
    resources["launch_configs"] = get_launch_configs()
    resources["notifications"] = get_notification_configs()
    resources["policies"] = get_policies()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_autoscaling_group():
    fields = ["AutoScalingGroupName", "AutoScalingGroupARN", "LaunchConfigurationName"]
    return get_service("describe_auto_scaling_groups", "AutoScalingGroups", fields)


def get_autoscaling_instances():
    fields = ["InstanceId", "AutoScalingGroupName", "ProtectedFromScaleIn"]
    return get_service("describe_auto_scaling_instances", "AutoScalingInstances", fields)


def get_launch_configs():
    fields = ["LaunchConfigurationName", "LaunchConfigurationARN", "ImageId", "InstanceType"]
    return get_service("describe_launch_configurations", "LaunchConfigurations", fields)


def get_notification_configs():
    fields = []
    return get_service("describe_notification_configurations", "NotificationConfigurations", fields)


def get_policies():
    fields = ["AutoScalingGroupName", "PolicyName", "PolicyARN", "PolicyType"]
    return get_service("describe_policies", "ScalingPolicies", fields)
