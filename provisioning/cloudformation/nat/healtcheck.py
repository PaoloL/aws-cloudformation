__version__     = "1.0"
__author__      = "Paolo Latella"
__email__       = "paolo.latella@xpeppers.com"

from boto import ec2
from boto import vpc 
import urllib2

REGION = 'eu-west-1'
RT = 'rtb-aa118bcf'
DESTINATION = '0.0.0.0/0'

#get instance medatadata
my_instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()


#disable source-destination check
connection_to_ec2 = ec2.connect_to_region(REGION)
connection_to_ec2.modify_instance_attribute(my_instance_id, attribute='sourceDestCheck', value=False)

#get the routing table
connection_to_vpc = vpc.connect_to_region(REGION)
connection_to_vpc.replace_route(RT, DESTINATION, instance_id=my_instance_id)
