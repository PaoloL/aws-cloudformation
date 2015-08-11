import json
import time
import boto.cloudformation as cloudformation
from boto import exception as boto_exception

REGION = 'eu-west-1'
INFRASTRUCTURE_FILE = './infrastructure.json'

def read_conf(path):
    with open(path, 'r') as f:
        return f.read().replace('\n', '')

def format_parameters(param_list):
    return [[param['ParameterKey'], param['ParameterValue']] for param in param_list]

def get_status_of_stack(stack,connection):
    describe_of_stack = connection.describe_stacks(stack)[0]
    return describe_of_stack.stack_status

def get_output_of_stack(stack,connection):
    describe_of_stack = connection.describe_stacks(stack)[0]
    return describe_of_stack.outputs

def resolve_dependencies(parameters_file, dependencies, connection):
    parameters_string = read_conf(parameters_file)
    parameters_list = json.loads(parameters_string)
    for parameter in parameters_list:
        for depend in dependencies:
            for mapping in depend['mapping']:
                if parameter['ParameterKey'] == mapping['input']:
                    for output in get_output_of_stack(depend['stack'],connection):
                        if output.key == mapping['output']: 
                            parameter['ParameterValue'] = output.value
    return json.dumps(parameters_list)
            

def create_tier(stack_name,template_file,parameters_list,connection): 
    template_string = read_conf(template_file)
    try:
        stack_id = connection.create_stack(stack_name, template_string, parameters=parameters_list)
        return stack_id
    except boto_exception as ex: 
        return ex.messages()

def create_infrastructure(infrastructure_file,connection):
    infrastructure_string = read_conf(infrastructure_file)
    infrastructure_json = json.loads(infrastructure_string)
    for tier in infrastructure_json['stacks']:
        print "CREATING " + tier['name'] + " with template file " + tier['template_file'] + " and parameters file " + tier['parameters_file']
        if len(tier['dependencies']) > 0:
            print "Tier " + tier['name'] + " has " + str(len(tier['dependencies'])) + " dependencies, resolving ..."
            parameters_list = format_parameters(json.loads(resolve_dependencies(tier['parameters_file'], tier['dependencies'],connection)))
        else:
            print "Tier " + tier['name'] + " has no dependencies" 
            parameters_list = format_parameters(json.loads(read_conf(tier['parameters_file'])))
        stack_id = create_tier(tier['name'],tier['template_file'],parameters_list,connection)
        status = str(get_status_of_stack(stack_id,connection))
        while status != 'CREATE_COMPLETE':
            time.sleep(10)
            status = str(get_status_of_stack(stack_id,connection))
            if status == "CREATE_FAILED" or status.startswith("ROLLBACK"):
                print "ERROR Create Failed"
                return



def main():
    #make a cloudformation connection
    cf_connection = cloudformation.connect_to_region(REGION)
    create_infrastructure(INFRASTRUCTURE_FILE,cf_connection)

if __name__ == '__main__':
    main()
