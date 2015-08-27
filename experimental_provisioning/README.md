#  Cloudformation and Boto
## Aternative approach to Stacks creation

In this post i would like to introduce an alternative approach to this practice: decompose the template to smaller template, one for each tier and add a file (JSON) that describe which tier should be active, the relative template and parameters file and what are its relations with the other tiers. A python script will resolve dependencies between tier tha we decided to create. 
