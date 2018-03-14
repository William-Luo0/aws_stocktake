import filter_keys
import boto3
from botocore.exceptions import ClientError

def get_service(function, dict_key, fields, extra_options={}):
  return filter_keys.filter_key('acm', function, dict_key, fields,
      extra_options)

def get_all(remove_empty=False):
  # Return all resources
  resources = {}
  resources["certificates"] = get_cert()

  if remove_empty:
    resources = dict((key,value) for key,value in resources.items() if value)

  return resources

def get_cert():
  fields = ["CertificateArn", "DomainName"]
  return get_service("list_certificates", "CertificateSummaryList", fields)
