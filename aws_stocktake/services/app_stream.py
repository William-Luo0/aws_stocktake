import filter_keys
import boto3
from botocore.exceptions import ClientError

def get_service(function, dict_key, fields, extra_options={}):
  return filter_keys.filter_key('appstream', function, dict_key, fields,
      extra_options)

def get_all(remove_empty=False):
  # Return all resources
  resources = {}
  resources["directory_configs"] = get_directory_configs()
  resources["app_fleets"] = get_fleets()
  resources["image_builders"] = get_image_builders()
  resources["images"] = get_images()
  resources["stacks"] = get_stacks()

  if remove_empty:
    resources = dict((key,value) for key,value in resources.items() if value)

  return resources

def get_directory_configs():
  fields = ["DirectoryName"]
  return get_service("describe_directory_configs", "DirectoryConfigs", fields)

def get_fleets():
  fields = ["Arn", "Name", "Description", "InstanceType"]
  return get_service("describe_fleets", "Fleets", fields)

def get_image_builders():
  fields = ["Arn", "Name", "Description", "InstanceType"]
  return get_service("describe_image_builders", "ImageBuilders", fields)

def get_images():
  fields = ["Arn", "Name", "Description", "Applications"]
  return get_service("describe_images", "Images", fields)

def get_stacks():
  fields = ["Arn", "Name", "Description"]
  return get_service("describe_stacks", "Stacks", fields)

