import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('batch', function, dict_key, fields,
                                  extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["compute_environments"] = get_compute_environments()
    resources["job_definitions"] = get_job_definitions()
    resources["job_queues"] = get_job_queues()

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_compute_environments():
    fields = ["computeEnvironmentName", "computeEnviironmentArn", "ecsClusterArn", "state", "serviceRole"]
    return get_service("describe_compute_environments", "computeEnvironments", fields)


def get_job_definitions():
    fields = ["jobDefinitionsName", "jobDefinitionsArn", "revision", "status", "type"]
    return get_service("describe_job_definitions", "jobDefinitions", fields)


def get_job_queues():
    fields = ["jobQueueName", "jobQueueArn", "state", "status"]
    return get_service("describe_job_queues", "jobQueues", fields)
