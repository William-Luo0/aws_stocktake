# Filters the output for the specified fields
import boto3

def filter_key(client, function, dict_key, fields, fnc_options={}):
  res = getattr(boto3.client(client), function)
  if bool(fnc_options):
    res = res(**fnc_options)
  else:
    res = res()
  res = res[dict_key]
  res[:] = [{key:value for key,value in i.items() if key in fields}
            for i in res]
  return res
