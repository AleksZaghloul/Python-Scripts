#!/usr/bin/env python3
import subprocess
import json
import os

#the command to find the ID and Environment tag of all instances - the tag is null if doesn't exist
list_instances = "aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:InstanceId,Environment:Tags[?Key==`Environment`] | [0].Value}'"

#parse the json output so python can understand
instances = json.loads(subprocess.getoutput(list_instances))

#a string of uncompliant instance ID's - begins empty
bad_instances = ""
count = 0

#loop through json output and add all ID's where the environment tag is NONE
#  - the json file is a bit awkward, it's a list of lists of dictionaries
for instance in instances:
    if instance[0]["Environment"] == None:
        #adds ID in a format easy to use with the command later - ID's separated by spaces
        bad_instances += instance[0]["ID"]
        bad_instances += " "
        count += 1 

#if instances found, terminate them
if count > 0:
    os.system("aws ec2 terminate-instances --instance-ids " + bad_instances) # + " --dry-run" for practice
    print("Terminated {} instances".format(count))
else:
    print("All instances are compliant")