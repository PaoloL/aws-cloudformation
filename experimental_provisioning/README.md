#  Cloudformation and Boto
## Aternative approach to Stacks creation

In this post i would like to introduce an alternative approach to this practice: decompose the template to smaller template, one for each tier and add a file (JSON) that describe which tier should be active, the relative template and parameters file and what are its relations with the other tiers. A python script will resolve dependencies between tier tha we decided to create.

### infrastructure.json

In this file we have a list of stacks to create (if stack is not defined will be not created). Each stack has a name, a template file and parameters file and relative dependencies from other stacks/tier. A dependencies is an array of dependent stack and relative resources mappings. For example the demo-preproduction-cache stack has a relationship with demo-preproduction-web stack where the security group created during web stack creation is an input for demo-preproduction-cache, because the security group of Elasticache cluster accept connection only from security group of EC2 instances on WEB Tier. For example output of Web Stack

```
"Outputs" : {
  "SecurityGroup" : 
   {
    "Description" : "Security Group Instance",
    "Value" : 
      { 
        "Ref" : "WebServerInstanceSecurityGroup" 
      }
   }
}
```

is now an input for Elasticache stack

```
BackendInstanceSecurityGroup" : 
{ 
  "Type" : "String" 
}
```

and dependencies are resolved by this description

```
"dependencies": 
[
  {
    "stack": "demo-preproduction-web",
    "mapping": 
    [ 
      { 
        "output": "SecurityGroup", 
        "input": "BackendInstanceSecurityGroup" 
      } 
    ]
  } 
]
```


### wrapper.py

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
