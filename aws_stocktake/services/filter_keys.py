# Filters the output for the specified fields
import boto3
from botocore.exceptions import ClientError

def filter_key(service, function, dict_key, fields, fnc_options={}):
  resource = []
  for region in get_regions(service):

    # Handle the error when operation not available in region or needs opt-in
    try:
      res = getattr(boto3.client(service, region), function)
      if bool(fnc_options):
        res = res(**fnc_options)
      else:
        res = res()

      # Filter out first level dict key
      if dict_key:
        res = res[dict_key]

      # Filter out dict keys inside lists
      if fields:
        res[:] = [{key:value for key,value in i.items() if key in fields}
                  for i in res]

      for item in res:
        item.update({"Region": region})
      resource.extend(res)

    except ClientError as e:
      # Error code explanations:
      # AccessDeniedException - Account isn't authorised to perform action
      if e.response["Error"]["Code"] in ("AuthFailure", "OptInRequired",
                                         "NotFoundException",
                                         "BadRequestException",
                                         "AccessDeniedException"):
        res = [{"Error": e.response["Error"]["Code"],
                "Description": e.response["Error"]["Message"],
                "Region": region,
                "Service": service,
                "Function": function}]
        # resource.extend(res)
      elif e.response["Error"]["Code"] != "UnsupportedOperation":
        raise

  return resource

def get_regions(service):
  return boto3.session.Session().get_available_regions(service)

