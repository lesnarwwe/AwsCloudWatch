import boto3
import json
import sys
import logging
import logging.config

logging.config.fileConfig("log.ini")
logger = logging.getLogger('sLogger')

client=boto3.client('cloudwatch')
ec=boto3.client('ec2')

logger.info("Passing parameters to the python script for generation of CloudWatch Alarms based on Thresholds")

args = sys.argv[1:]

if args:
    logger.info("We can proceed with the script execution")
else:
    print("Please pass parameter while setting up the alarms\nFormat for production alert setup - python functional_approach.py prod.json\nFormat for non-production alert setup - python functional_approach.py non-prod.json")
    logger.info("Exiting without execution need parameters while running the script")
    exit()

logger.info("Reading the contents of input file")

with open( sys.argv[1], 'r') as f:
    contents = f.read()

dict = json.loads(contents)
cpu_td=dict['CPU_Threshold']
cpu_pd=dict['CPU_Period']
cpu_ep=dict['CPU_EvaluationPeriods']

logger.info("Checking whether Environment is Prod/Non-Prod")


def main():
    
    env_type = dict['Env']

    if env_type == 'Prod':
        logger.info("Enviroment is Prod, setting up alerts for Production Infra")
        prod_func()

    else:
        logger.info("Environment is Non-Prod, setting up alerts for Non-Production Infra")
        dev_func()

def prod_func():

    
    logger.info("Filtering instanes based on tags")
    response=ec.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Env',
                    'Values': [
                        'Prod',
                    ]
                }])

    logger.info("Checking all the VM's in a region - we will get alerts for those VM's which are Running")

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            id = instance['InstanceId']
            hostname = instance['PrivateDnsName']
            for t in instance['Tags']:
                if t['Key'] == 'Name':
                    iname = t['Value']
                    
                    logger.info("Checking CPU utilization, we will create alarms if it exceeds threshold")
    
                    cpu_alarm = client.put_metric_alarm(
                        AlarmName= 'CPUAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='CPUUtilization',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:SubscriptionTest-SNSTopic-YB161YY7ID21'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Percent'
                    )
                    
                    
                    print("CPU Alarm Status for InstanceName" + iname)
                    print(cpu_alarm)
                    
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    cpu_alarm_reset = client.set_alarm_state(
                    AlarmName='CPUAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )
            
                    
                    logger.info("Checking Disk ReadOps, we will create alarms if it exceeds threshold")

                    diskreadops_alarm = client.put_metric_alarm(
                        AlarmName= 'DiskReadOpsAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='DiskReadOps',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
                    print("DiskReadOps Alarm Status for InstanceName" + iname)
                    print(diskreadops_alarm)
                    
                                        
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    
                    diskreadops_alarm_reset = client.set_alarm_state(
                    AlarmName='DiskReadOpsAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )
        
                    
                    logger.info("Checking Disk WriteOps, we will trigger alarms if it exceeds threshold")
        
                    diskwriteops_alarm = client.put_metric_alarm(
                        AlarmName= 'DiskWriteOpsAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='DiskWriteOps',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
                    print("DiskWriteOpsOps Alarm Status for InstanceName" + iname)
                    print(diskwriteops_alarm)

                                    
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                        
                    diskwriteops_alarm_reset = client.set_alarm_state(
                    AlarmName='DiskWriteOpsAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking NetworkIn, we will trigger alarms if it exceeds threshold")
                    
                    NetworkIn_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkInAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkIn',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Bytes'
                    )
					
					print("NetworkIn Alarm Status for InstanceName" + iname)
                    print(NetworkIn_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkIn_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkInAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking NetworkPacketsIn, we will trigger alarms if it exceeds threshold")
                    
                    NetworkPacketsIn_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkPacketsInAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkPacketsIn',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("NetworkPacketsIn Alarm Status for InstanceName" + iname)
                    print(NetworkPacketsIn_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkPacketsIn_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkPacketsInAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
                    
                    logger.info("Checking NetworkPacketsOut, we will trigger alarms if it exceeds threshold")
					
                    NetworkPacketsOut_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkPacketsOutAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkPacketsOut',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("NetworkPacketsOut Alarm Status for InstanceName" + iname)
                    print(NetworkPacketsOut_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkPacketsOut_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkPacketsOutAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailedAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					
					print("StatusCheckFailed Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    
                    StatusCheckFailed_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailedAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed_Instance, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_Instance_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailed_InstanceAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed_Instance',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					
					print("StatusCheckFailed_Instance Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_Instance_alarm)
					
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    StatusCheckFailed_Instance_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailed_InstanceAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed_System, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_System_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailed_SystemAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed_System',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("StatusCheckFailed_System Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_System_alarm)
					
					logger.info("Checking StatusCheckFailed_Instance, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_System_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailed_SystemAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
                

def dev_func():
    
    response=ec.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Env',
                    'Values': [
                        'Non-Prod',
                    ]
                }])

    logger.info("Checking all the VM's in a region - we will get alerts for those VM's which are Running")

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            id = instance['InstanceId']
            hostname = instance['PrivateDnsName']
            for t in instance['Tags']:
                if t['Key'] == 'Name':
                    iname = t['Value']
                    
                    logger.info("Checking CPU utilization, we will create alarms if it exceeds threshold")
    
                    cpu_alarm = client.put_metric_alarm(
                        AlarmName= 'CPUAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='CPUUtilization',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:SubscriptionTest-SNSTopic-YB161YY7ID21'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Percent'
                    )
                    
                    
                    print("CPU Alarm Status for InstanceName" + iname)
                    print(cpu_alarm)
                    
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    cpu_alarm_reset = client.set_alarm_state(
                    AlarmName='CPUAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )
            
                    
                    logger.info("Checking Disk ReadOps, we will create alarms if it exceeds threshold")

                    diskreadops_alarm = client.put_metric_alarm(
                        AlarmName= 'DiskReadOpsAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='DiskReadOps',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
                    print("DiskReadOps Alarm Status for InstanceName" + iname)
                    print(diskreadops_alarm)
                    
                                        
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    
                    diskreadops_alarm_reset = client.set_alarm_state(
                    AlarmName='DiskReadOpsAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )
        
                    
                    logger.info("Checking Disk WriteOps, we will trigger alarms if it exceeds threshold")
        
                    diskwriteops_alarm = client.put_metric_alarm(
                        AlarmName= 'DiskWriteOpsAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='DiskWriteOps',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
                    print("DiskWriteOpsOps Alarm Status for InstanceName" + iname)
                    print(diskwriteops_alarm)

                                    
                    logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                        
                    diskwriteops_alarm_reset = client.set_alarm_state(
                    AlarmName='DiskWriteOpsAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking NetworkIn, we will trigger alarms if it exceeds threshold")
                    
                    NetworkIn_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkInAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkIn',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Bytes'
                    )
					
					print("NetworkIn Alarm Status for InstanceName" + iname)
                    print(NetworkIn_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkIn_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkInAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking NetworkPacketsIn, we will trigger alarms if it exceeds threshold")
                    
                    NetworkPacketsIn_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkPacketsInAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkPacketsIn',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("NetworkPacketsIn Alarm Status for InstanceName" + iname)
                    print(NetworkPacketsIn_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkPacketsIn_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkPacketsInAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
                    
                    logger.info("Checking NetworkPacketsOut, we will trigger alarms if it exceeds threshold")
					
                    NetworkPacketsOut_alarm = client.put_metric_alarm(
                        AlarmName= 'NetworkPacketsOutAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='NetworkPacketsOut',
                        Namespace='AWS/EC2',
                        Statistic='Average',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=cpu_td,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("NetworkPacketsOut Alarm Status for InstanceName" + iname)
                    print(NetworkPacketsOut_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    NetworkPacketsOut_alarm_reset = client.set_alarm_state(
                    AlarmName='NetworkPacketsOutAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailedAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					
					print("StatusCheckFailed Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_alarm)
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    
                    StatusCheckFailed_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailedAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed_Instance, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_Instance_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailed_InstanceAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed_Instance',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					
					print("StatusCheckFailed_Instance Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_Instance_alarm)
					
					
					logger.info("Alarm has been triggered, so resetting the alarm state to OK")
                    
                    StatusCheckFailed_Instance_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailed_InstanceAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )

                    
					logger.info("Checking StatusCheckFailed_System, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_System_alarm = client.put_metric_alarm(
                        AlarmName= 'StatusCheckFailed_SystemAlarm' + iname,
                        AlarmDescription= hostname,
                        #InstanceName= iname,
                        MetricName='StatusCheckFailed_System',
                        Namespace='AWS/EC2',
                        Statistic='Maximum',
                        ComparisonOperator='GreaterThanOrEqualToThreshold',
                        Threshold=1,
                        Period=cpu_pd,
                        EvaluationPeriods=cpu_ep,
                        ActionsEnabled=True,
                        AlarmActions=[
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:notify1', 
                            'arn:aws:sns:ap-south-1:{ AWS Subscription ID }:VR_AWS_Monitoring'
                            ],
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': id
                               
                            },
                            
                        ],
                        Unit='Count'
                    )
					print("StatusCheckFailed_System Alarm Status for InstanceName" + iname)
                    print(StatusCheckFailed_System_alarm)
					
					logger.info("Checking StatusCheckFailed_Instance, we will trigger alarms if it exceeds threshold")
                    
                    StatusCheckFailed_System_alarm_reset = client.set_alarm_state(
                    AlarmName='StatusCheckFailed_SystemAlarm' + iname,
                    StateValue='OK',
                    StateReason='Reset'
                    )


if __name__ == '__main__': main()
