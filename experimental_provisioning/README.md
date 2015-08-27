#  Cloudformation and Boto
## Aternative approach to Stacks creation

In this post i would like to introduce an alternative approach to this practice: decompose the template to smaller template, one for each tier and add a file (JSON) that describe which tier should be active, the relative template and parameters file and what are its relations with the other tiers. A python script will resolve dependencies between tier tha we decided to create.

'''
maverick$ python wrapper.py
CREATING demo-preproduction-elb with template file ./cloudformation/elb/elb.json and parameters file ./cloudformation/elb/preproduction.json
Tier demo-preproduction-elb has no dependencies
Tier demo-preproduction-elb has no fix
CREATING demo-preproduction-web with template file ./cloudformation/web/web.json and parameters file ./cloudformation/web/preproduction.json
Tier demo-preproduction-web has 1 dependencies, resolving ...
Tier demo-preproduction-web has no fix
CREATING demo-preproduction-cache with template file ./cloudformation/elasticache/elasticache.json and parameters file ./cloudformation/elasticache/preproduction.json
Tier demo-preproduction-cache has 1 dependencies, resolving ...
Tier demo-preproduction-cache has 1 fix, fixing now ...
''' 
