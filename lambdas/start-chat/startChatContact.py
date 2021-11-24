import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SSM = boto3.client('ssm')
connect = boto3.client('connect')

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))
    body = event['body']
    
    responseFromSSM = SSM.get_parameter(Name="hlc302-connect-instance-id")
    instance_id = responseFromSSM['Parameter']['Value']
    logger.info(instance_id)
    
    responseFromSSM = SSM.get_parameter(Name="hlc302-flow-id")
    flow_parameter = responseFromSSM['Parameter']['Value']
    logger.info(flow_parameter)
    
    json_body = json.loads(body)
    return startChatContact(json_body, instance_id, flow_parameter)
    

def startChatContact(body, instanceId, contactFlowId):
    try: 
        response = connect.start_chat_contact(InstanceId=instanceId, 
            ContactFlowId=contactFlowId, 
            Attributes={"customerName": body['ParticipantDetails']['DisplayName'] },
            ParticipantDetails={"DisplayName": body['ParticipantDetails']['DisplayName']}
        )
        logger.info('Start chat succeeded with the response ' + json.dumps(response))
        return buildSuccessfulResponse(response)
    except BaseException as err: 
        logger.error("Error starting the chat")
        return buildResponseFailed(err)

def buildSuccessfulResponse(result):
     response = {
         "isBase64Encoded": False,
         "statusCode": 200,
         "headers": {
             "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials' : "true",
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
         },
         "body": json.dumps({"data": {"startChatResult": result}})
     }
     logger.info("RESPONSE " + json.dumps(response))
     return response
     
def buildResponseFailed(err):
    response = {
        "isBase64Encoded": False,
        "statusCode": 500,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials' : "true",
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        },
        "body": json.dumps({"data": {" Error": err}})
    }
    logger.info("ERROR RESPONSE " + str(err))
    return response