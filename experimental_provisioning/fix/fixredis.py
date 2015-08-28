import json
import time
import boto.cloudformation as cloudformation
from boto import exception as boto_exception
import boto3
import sys


REGION = 'eu-west-1'
PROJECT = 'ipanel'
ENVIRONMENT = 'preproduction'
SERVICE = 'redis'
ROLE = 'api'

arn = 'arn:aws:elasticache:eu-west-1:554957483970:cluster:'

def construct_tags (project=PROJECT, env=ENVIRONMENT, service=SERVICE, role=ROLE):
	tags = []
	values = [PROJECT, ENVIRONMENT, SERVICE, ROLE]
	name = '%s-%s-%s-%s' % (PROJECT, ENVIRONMENT, SERVICE, ROLE)
	element = { 'Key': 'Name', 'Value': name }
	tags.append(element)
	count = 0
	for tag in ('Project', 'Environment', 'Service', 'Role'):
		element = {'Key': tag, 'Value': str(values[count])}
		tags.append(element)
		count = count + 1
	return tags

def get_cluster_id(stack_name):
	cf_connection = cloudformation.connect_to_region(REGION)
	resources = cf_connection.list_stack_resources(stack_name)
	for resource in resources:
		if resource.logical_resource_id == "RedisReplicationGroup":
			return resource.physical_resource_id

def tag_redis_resources(cluster_id):
	client = boto3.client('elasticache',REGION)
	Tags = construct_tags()
	#for node in cluster
	replication_group = client.describe_replication_groups(ReplicationGroupId=cluster_id)
	for group in replication_group['ReplicationGroups']:
		for node in group['NodeGroups']:
			for member in node['NodeGroupMembers']:
				resource = arn+member['CacheClusterId']
				response = client.add_tags_to_resource(ResourceName=resource,Tags=Tags)
	return response

def main(argv):
	stack_name = argv[1]
	tag_redis_resources(get_cluster_id(stack_name))

if __name__ == '__main__':
    main(sys.argv)

