import json
import boto3

def lambda_handler(event, context):    
    if 'Tags' in event['detail'] and 'application-autoscaling:resourceId' in event['detail']['Tags']:
        try:
            resource_identifier = event['detail']['SourceArn']
            cluster_id = event['detail']['Tags']['application-autoscaling:resourceId']
            account = event['account']
            region = event['region']
            rds = boto3.client('rds', region_name=region)
            cluster_arn='arn:aws:rds:'+region+':'+account+':'+cluster_id
            cluster_tags = rds.list_tags_for_resource(ResourceName=cluster_arn,)['TagList']
            response = rds.describe_db_instances(DBInstanceIdentifier=resource_identifier)
            autoscaling_tags=response['DBInstances'][0]['TagList']
            for cluster_tag in cluster_tags:
                if cluster_tag not in autoscaling_tags:
                    response = rds.add_tags_to_resource(ResourceName=event['detail']['SourceArn'], Tags=[cluster_tag])
        except Exception as e:
            print (e)
