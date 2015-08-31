# High Availability on NAT Instance 

On AWS instances on private subnets should not be directly addressable from the Internet. In this case we need NAT instance in public subent for routing the traffic coming out from private instances. A NAT instance can introduce a single point of failure to our VPC's, then is important to create a High Availability solution. Below a solution that use a Cloudformation template for 1:1 Autoscaling group using a python script that update routing table in case of failover. This is an alternative to the solution described by [Jinesh Varia] (http://aws.amazon.com/articles/2781451301784570)

## Template Cloudformation

nat.json is a template that implement the solution. The file preproduction.json is a parameters file, in particular this file configure the following parameters importa for failover:
* VpcId: is the id of VPC that contains the instances and relative public and private subnet 
* BackEndRouteTable: this the route table that Backend instances using for routing, this is the table that NAT istance update in case of failover
* InstanceRole: this is a IAM role necessary for update the routing table via python script using boto SDK
* Subnets: this is the subnets of the AZ vill be spawned (insert least two subnet on two different AZ)
* AmiId: this is id of AMI configured with routing rules, may be the instance suggested from AWS

## Python Script

The script healthcheck.py executed by userdata retrieve info from metadata, diable source-destination check and update the routing table taking the routing
