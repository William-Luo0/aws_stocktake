# All the ec2 related functions
import filter_keys
import boto3
from botocore.exceptions import ClientError


def get_service(function, dict_key, fields, extra_options={}):
    return filter_keys.filter_key('ec2', function, dict_key, fields, extra_options)


def get_all(remove_empty=False):
    # Return all resources
    resources = {}
    resources["connection_notifications"] = get_connection_notifications()
    resources["dedicated"] = get_dedicated()
    resources["dhcp_options"] = get_dhcp_options()
    resources["ec2_amis"] = get_ec2_amis()
    resources["egress_igs"] = get_egress_igs()
    resources["eips"] = get_eips()
    resources["elastic_gpus"] = get_elastic_gpus()
    resources["endpoint_connections"] = get_endpoint_connections()
    resources["endpoint_service_configs"] = get_endpoint_service_configs()
    resources["endpoints"] = get_endpoints()
    resources["flow_logs"] = get_flow_logs()
    # For some reason FPGA is not valid for the ec2 service but is documented
    # resources["fpga_images"] = get_fpga_images()
    resources["igs"] = get_igs()
    resources["instances"] = get_instances()
    resources["keys"] = get_keys()
    resources["launch_templates"] = get_launch_templates()
    resources["nacls"] = get_nacls()
    resources["nat_gateways"] = get_nat_gateways()
    resources["network_interfaces"] = get_network_interfaces()
    resources["peering_connections"] = get_peering_connections()
    resources["placement_groups"] = get_placement_groups()
    resources["prefix_lists"] = get_prefix_lists()
    resources["reserved"] = get_reserved()
    resources["reserved_listings"] = get_reserved_listings()
    resources["route_tables"] = get_route_tables()
    resources["scheduled"] = get_scheduled()
    resources["sgs"] = get_sgs()
    resources["snapshots"] = get_snapshots()
    resources["spot_fleets"] = get_spot_fleets()
    resources["spot_instances"] = get_spot_instances()
    resources["subnets"] = get_subnets()
    resources["tags"] = get_tags()
    resources["volumes"] = get_volumes()
    resources["vpcs"] = get_vpcs()
    resources["vpn_connections"] = get_vpn_connections()
    resources["vpn_gateways"] = get_vpn_gateways()
    resources["vpns"] = get_vpns()
    resources["valid_regions"] = filter_keys.get_regions("ec2")

    if remove_empty:
        resources = dict((key, value) for key, value in resources.items() if value)

    return resources


def get_eips():
    fields = ["InstanceId", "PublicIP", "PrivateIpAddress", "Domain"]
    return get_service("describe_addresses", "Addresses", fields)


def get_vpns():
    fields = ["CustomerGatewayId", "IpAddress", "Type", "BgpAsn"]
    return get_service("describe_customer_gateways", "CustomerGateways", fields)


def get_dhcp_options():
    fields = ["DhcpOptionsId"]
    return get_service("describe_dhcp_options", "DhcpOptions", fields)


def get_egress_igs():
    fields = ["EgressOnlyInternetGatewayId"]
    return get_service("describe_egress_only_internet_gateways", "EgressOnlyInternetGateways", fields)


def get_elastic_gpus():
    fields = ["ElasticGpuId", "ElasticGpuType", "InstanceId", "ElasticGpuState"]
    return get_service("describe_elastic_gpus", "ElasticGpuSet", fields)


def get_flow_logs():
    fields = ["FlowLogId", "LogGroupName", "ResourceId"]
    return get_service("describe_flow_logs", "FlowLogs", fields)


def get_fpga_images():
    fields = ["Name", "FpgaImageId", "FpgaImageGlobalId"]
    return get_service("describe_fpga_images", "FpgaImages", fields, {"Owners": ["self"]})


def get_dedicated():
    fields = ["HostId", "HostReservationId", "Instances"]
    return get_service("describe_hosts", "Hosts", fields)


def get_ec2_amis():
    fields = ["Name", "ImageId"]
    return get_service("describe_images", "Images", fields, {"Owners": ["self"]})


def get_instances():
    fields = ["InstanceId", "InstanceType", "ImageId", "LaunchTime", "Tags"]
    resources = []
    for region in filter_keys.get_regions("ec2"):
        res = boto3.client("ec2", region).describe_instances()
        res = res["Reservations"]
        instances = []
        for item in res:
            instances.extend(item["Instances"])
        instances[:] = [{key: value for key, value in i.items() if key in fields}
                        for i in instances]
        resources.extend(instances)
    return resources


def get_igs():
    fields = ["InternetGatewayId", "Attachments"]
    return get_service("describe_internet_gateways", "InternetGateways", fields)


def get_keys():
    fields = ["KeyFingerprint", "KeyName"]
    return get_service("describe_key_pairs", "KeyPairs", fields)


def get_launch_templates():
    fields = ["LaunchTemplateId", "LaunchTemplateName"]
    return get_service("describe_launch_templates", "LaunchTemplates", fields)


def get_nat_gateways():
    fields = ["NatGatewayId", "NatGatewayAddresses"]
    return get_service("describe_nat_gateways", "NatGateways", fields)


def get_nacls():
    fields = ["NetworkAclId", "VpcId"]
    return get_service("describe_network_acls", "NetworkAcls", fields)


def get_network_interfaces():
    fields = ["NetworkInterfaceId", "VpcId", "OwnerId", "RequesterId"]
    return get_service("describe_network_interfaces", "NetworkInterfaces", fields)


def get_placement_groups():
    fields = ["GroupName", "Strategy"]
    return get_service("describe_placement_groups", "PlacementGroups", fields)


def get_prefix_lists():
    fields = ["PrefixListId", "PrefixListName"]
    return get_service("describe_prefix_lists", "PrefixLists", fields)


def get_reserved():
    fields = ["ReservedInstancesId", "FixedPrice", "UsagePrice", "InstanceCount", "InstanceType"]
    return get_service("describe_reserved_instances", "ReservedInstances", fields)


def get_reserved_listings():
    fields = ["ReservedInstancesId", "ReservedInstancesListingId"]
    return get_service("describe_reserved_instances_listings", "ReservedInstancesListings", fields)


def get_route_tables():
    fields = ["RouteTableId", "VpcId", "Routes"]
    return get_service("describe_route_tables", "RouteTables", fields)


def get_scheduled():
    fields = ["ScheduledInstanceId", "InstanceCount", "HourlyPrice"]
    return get_service("describe_scheduled_instances", "ScheduledInstanceSet",
                       fields)


def get_sgs():
    fields = ["GroupName", "GroupId", "VpcId"]
    return get_service("describe_security_groups", "SecurityGroups", fields)


def get_snapshots():
    fields = ["VolumeId", "SnapshotId", "VolumeSize"]
    return get_service("describe_snapshots", "Snapshots", fields,
                       {"OwnerIds": ["self"]})


def get_spot_fleets():
    fields = ["ActivityStatus", "SpotFleetRequestId", "SpotFleetRequestState"]
    return get_service("describe_spot_fleet_requests", "SpotFleetRequestConfigs",
                       fields)


def get_spot_instances():
    fields = ["SpotInstanceRequestId", "SpotPrice", "State"]
    return get_service("describe_spot_instance_requests", "SpotInstanceRequests", fields)


def get_subnets():
    fields = ["SubnetId", "VpcId", "CidrBlock"]
    return get_service("describe_subnets", "Subnets", fields)


def get_tags():
    fields = ["Key", "ResourceId", "ResourceType", "Value"]
    return get_service("describe_tags", "Tags", fields)


def get_volumes():
    fields = ["VolumeId", "SnapshotId", "Size"]
    return get_service("describe_volumes", "Volumes", fields)


def get_connection_notifications():
    fields = ["ConnectionNotificationArn", "ConnectionNotificationId",
              "VpcEndpointId", "ServiceId"]
    return get_service("describe_vpc_endpoint_connection_notifications",
                       "ConnectionNotificationSet", fields)


def get_endpoint_connections():
    fields = ["VpcEndpointId", "VpcEndpointOwner", "ServiceId",
              "VpcEndpointState"]
    return get_service("describe_vpc_endpoint_connections",
                       "VpcEndpointConnections", fields)


def get_endpoint_service_configs():
    fields = ["ServiceId", "ServiceName", "ServiceState"]
    return get_service("describe_vpc_endpoint_service_configurations",
                       "ServiceConfigurations", fields)


def get_endpoints():
    fields = ["VpcEndpointId", "VpcId", "VpcEndpointType"]
    return get_service("describe_vpc_endpoints", "VpcEndpoints", fields)


def get_peering_connections():
    fields = ["VpcPeeringConnectionId", "Tags", "Status"]
    return get_service("describe_vpc_peering_connections", "VpcPeeringConnections", fields)


def get_vpcs():
    fields = ["VpcId", "CidrBlock"]
    return get_service("describe_vpcs", "Vpcs", fields)


def get_vpn_connections():
    fields = ["VpnConnectionId", "VpnGatewayId", "CustomerGatewayId"]
    return get_service("describe_vpn_connections", "VpnConnections", fields)


def get_vpn_gateways():
    fields = ["VpnGatewayId", "AmazonSideAsn", "Type"]
    return get_service("describe_vpn_gateways", "VpnGateways", fields)
