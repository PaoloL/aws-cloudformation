#  Cloudformation and Boto
## Aternative approach to Stacks creation

I would like to introduce an alternative approach to this practice: decompose a monolithic cloudformation template in to smaller template, one for each tier, and add a file (JSON) that describe which tier should be active/created, the relative template and parameters file, what are its relations with the other tiers and eventually script to execute for fix missing action on Cloudformation Engine. We have a JSON file that describe the acrhitecture (the tiers of our architecture and relative dependencies and fix) plus a python script that parse this file and resolve denpendencie and launch fix modules.

### infrastructure.json

In this file we have a list of stacks to create (if stack is note defined will be not created). Each stack has a name, a template file, a parameters file and an array of dependencies and fix. The array of dependencies is a set of dependency from other stacks/tier, for example the security group in output created during web stack creation is an input for demo-preproduction-cache, because the security group of Elasticache cluster accept connection only from security group of EC2 instances on WEB Tier. The array of fix is a set di python modules that will be executed for fix missing action on Cloudformation service. For example with fix module we can tag the elasticache cluster, infact at this moment the tags on elasticache cluster are not supported by Cloudformation.  


This is an example of stack with dependencies and fixe

```
{
      "name": "demo-preproduction-cache",
      "template_file": "./cloudformation/elasticache/elasticache.json",
      "parameters_file": "./cloudformation/elasticache/preproduction.json",
      "dependencies": [
        {
          "stack": "demo-preproduction-web",
          "mapping": [
            {
              "output": "SecurityGroup",
              "input": "BackendInstanceSecurityGroup"
            }
          ]
        }
      ],
      "fix" : [
        {
          "fix_file" : "fix/fixredis.py"
        }
      ]
    }
```


### wrapper.py

The wrapper.py script is the root of our logic. The script parse infrastructure.json file retrieve the stacks that must to be create, resolve dependencies and execute fix.

```
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
``` 
