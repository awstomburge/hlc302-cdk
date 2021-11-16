# standard imports
import sys, logging, traceback, json, time

# custom imports
import boto3
from crhelper import CfnResource

# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# helpers
helper = CfnResource(
	json_logging=False,
	log_level='DEBUG', 
	boto_level='CRITICAL'
)

# client
connect_client = boto3.client('connect')
ssm_client = boto3.client('ssm')

@helper.create
def create(event, context):
    logger.info("Got Create")

    connect_instance_id = ssm_client.get_parameter(
        Name='hlc302-connect-instance-id'
    )

    # with open('chime-connect-integration-flow.json', 'r') as json_file:
    #     data = json.loads(json_file.read())

    response = connect_client.create_contact_flow(
        InstanceId=connect_instance_id['Parameter']['Value'],
        Name='Chime Connect Integration flow',
        Type='CONTACT_FLOW',
        # Content=json.dumps(data)
        Content="{\"Version\":\"2019-10-30\",\"StartAction\":\"52580d12-a281-4a32-b41a-0693f4798683\",\"Metadata\":{\"entryPointPosition\":{\"x\":20,\"y\":20},\"snapToGrid\":false,\"ActionMetadata\":{\"80d53f37-f69a-4726-a8e5-939fc6d59c2d\":{\"position\":{\"x\":318,\"y\":443},\"useDynamic\":false,\"queue\":{\"id\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/queue/fd220d05-3f3a-4755-b0ca-209c38e2db72\",\"text\":\"BasicQueue\"}},\"ab4f6f1d-6a40-46bf-a321-a73b9056544d\":{\"position\":{\"x\":605,\"y\":495},\"contactFlow\":{\"id\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/contact-flow/c7819258-e037-40b2-84c6-201f96f36c8d\",\"text\":\"Default customer queue\"},\"customerOrAgent\":true,\"useDynamic\":false},\"969fee59-08d3-4c30-a073-d6dad8028cf8\":{\"position\":{\"x\":862,\"y\":546},\"useDynamic\":false},\"b270d197-2183-4aee-abf5-f5fc323e8a9b\":{\"position\":{\"x\":48,\"y\":393},\"useDynamic\":false},\"52580d12-a281-4a32-b41a-0693f4798683\":{\"position\":{\"x\":158,\"y\":178}},\"64b5d89a-a1b6-4df5-b75c-b597cdf13b13\":{\"position\":{\"x\":393,\"y\":47},\"conditionMetadata\":[{\"id\":\"f7ffc417-c9de-4265-a4d0-92607987d40a\",\"value\":\"Video\"},{\"id\":\"2333c3c7-f46f-4081-906a-0be5c442e1b8\",\"value\":\"Chat\"}],\"useDynamic\":false,\"dynamicMetadata\":{},\"useDynamicLexBotArn\":false},\"2f2aa4e7-0b2c-4cb3-9bf7-3b888b6b689a\":{\"position\":{\"x\":646,\"y\":51},\"useDynamic\":false},\"a3fed5f3-a5fb-4eec-8534-2cf40982bde4\":{\"position\":{\"x\":887,\"y\":57},\"useDynamic\":false,\"queue\":{\"id\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/queue/fd220d05-3f3a-4755-b0ca-209c38e2db72\",\"text\":\"BasicQueue\"}},\"e5400ca1-9b31-4ec4-8e08-c5e14bd86ee1\":{\"position\":{\"x\":1440,\"y\":64},\"useDynamic\":false},\"34d8adda-f9fc-4df9-98a5-9721d352ecc0\":{\"position\":{\"x\":1180,\"y\":65},\"contactFlow\":{\"id\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/contact-flow/c7819258-e037-40b2-84c6-201f96f36c8d\",\"text\":\"Default customer queue\"},\"customerOrAgent\":true,\"useDynamic\":false},\"7535999b-bd7d-4efe-aada-688ecc9a8e37\":{\"position\":{\"x\":1314,\"y\":657},\"useDynamic\":false},\"487aace6-4ffe-4a1d-8b1d-3d14ce447931\":{\"position\":{\"x\":615,\"y\":318},\"useDynamic\":false},\"78596bf3-a6bc-4efc-9741-44104789fb3e\":{\"position\":{\"x\":1678,\"y\":259},\"useDynamic\":false},\"4b1c4159-1f57-4570-b96f-363f4a8132d4\":{\"position\":{\"x\":1923,\"y\":496}}}},\"Actions\":[{\"Identifier\":\"80d53f37-f69a-4726-a8e5-939fc6d59c2d\",\"Parameters\":{\"QueueId\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/queue/fd220d05-3f3a-4755-b0ca-209c38e2db72\"},\"Transitions\":{\"NextAction\":\"ab4f6f1d-6a40-46bf-a321-a73b9056544d\",\"Errors\":[{\"NextAction\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"ErrorType\":\"NoMatchingError\"}],\"Conditions\":[]},\"Type\":\"UpdateContactTargetQueue\"},{\"Identifier\":\"ab4f6f1d-6a40-46bf-a321-a73b9056544d\",\"Parameters\":{\"EventHooks\":{\"CustomerQueue\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/contact-flow/c7819258-e037-40b2-84c6-201f96f36c8d\"}},\"Transitions\":{\"NextAction\":\"969fee59-08d3-4c30-a073-d6dad8028cf8\",\"Errors\":[{\"NextAction\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"ErrorType\":\"NoMatchingError\"}],\"Conditions\":[]},\"Type\":\"UpdateContactEventHooks\"},{\"Identifier\":\"969fee59-08d3-4c30-a073-d6dad8028cf8\",\"Transitions\":{\"NextAction\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"Errors\":[{\"NextAction\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"ErrorType\":\"NoMatchingError\"},{\"NextAction\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"ErrorType\":\"QueueAtCapacity\"}],\"Conditions\":[]},\"Type\":\"TransferContactToQueue\"},{\"Identifier\":\"b270d197-2183-4aee-abf5-f5fc323e8a9b\",\"Parameters\":{\"Text\":\"Great! We will transfer you to an agent to chat.\"},\"Transitions\":{\"NextAction\":\"80d53f37-f69a-4726-a8e5-939fc6d59c2d\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"MessageParticipant\"},{\"Identifier\":\"52580d12-a281-4a32-b41a-0693f4798683\",\"Parameters\":{\"FlowLoggingBehavior\":\"Enabled\"},\"Transitions\":{\"NextAction\":\"64b5d89a-a1b6-4df5-b75c-b597cdf13b13\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"UpdateFlowLoggingBehavior\"},{\"Identifier\":\"64b5d89a-a1b6-4df5-b75c-b597cdf13b13\",\"Parameters\":{\"Text\":\"Would you like to do a video call or text chat? Type \\'chat\\' or \\'video\\'.\",\"LexBot\":{\"Name\":\"StartVideoCall\",\"Region\":\"us-east-1\",\"Alias\":\"$LATEST\"}},\"Transitions\":{\"NextAction\":\"487aace6-4ffe-4a1d-8b1d-3d14ce447931\",\"Errors\":[{\"NextAction\":\"487aace6-4ffe-4a1d-8b1d-3d14ce447931\",\"ErrorType\":\"NoMatchingError\"},{\"NextAction\":\"b270d197-2183-4aee-abf5-f5fc323e8a9b\",\"ErrorType\":\"NoMatchingCondition\"}],\"Conditions\":[{\"NextAction\":\"2f2aa4e7-0b2c-4cb3-9bf7-3b888b6b689a\",\"Condition\":{\"Operator\":\"Equals\",\"Operands\":[\"Video\"]}},{\"NextAction\":\"b270d197-2183-4aee-abf5-f5fc323e8a9b\",\"Condition\":{\"Operator\":\"Equals\",\"Operands\":[\"Chat\"]}}]},\"Type\":\"ConnectParticipantWithLexBot\"},{\"Identifier\":\"2f2aa4e7-0b2c-4cb3-9bf7-3b888b6b689a\",\"Parameters\":{\"Text\":\"Great! We will transfer you to an agent to do video.\"},\"Transitions\":{\"NextAction\":\"a3fed5f3-a5fb-4eec-8534-2cf40982bde4\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"MessageParticipant\"},{\"Identifier\":\"a3fed5f3-a5fb-4eec-8534-2cf40982bde4\",\"Parameters\":{\"QueueId\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/queue/fd220d05-3f3a-4755-b0ca-209c38e2db72\"},\"Transitions\":{\"NextAction\":\"34d8adda-f9fc-4df9-98a5-9721d352ecc0\",\"Errors\":[{\"NextAction\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"ErrorType\":\"NoMatchingError\"}],\"Conditions\":[]},\"Type\":\"UpdateContactTargetQueue\"},{\"Identifier\":\"e5400ca1-9b31-4ec4-8e08-c5e14bd86ee1\",\"Transitions\":{\"NextAction\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"Errors\":[{\"NextAction\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"ErrorType\":\"NoMatchingError\"},{\"NextAction\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"ErrorType\":\"QueueAtCapacity\"}],\"Conditions\":[]},\"Type\":\"TransferContactToQueue\"},{\"Identifier\":\"34d8adda-f9fc-4df9-98a5-9721d352ecc0\",\"Parameters\":{\"EventHooks\":{\"CustomerQueue\":\"arn:aws:connect:us-east-1:785787308789:instance/79a24403-e70e-47cd-970c-e81cb4d05ab2/contact-flow/c7819258-e037-40b2-84c6-201f96f36c8d\"}},\"Transitions\":{\"NextAction\":\"e5400ca1-9b31-4ec4-8e08-c5e14bd86ee1\",\"Errors\":[{\"NextAction\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"ErrorType\":\"NoMatchingError\"}],\"Conditions\":[]},\"Type\":\"UpdateContactEventHooks\"},{\"Identifier\":\"7535999b-bd7d-4efe-aada-688ecc9a8e37\",\"Parameters\":{\"Text\":\"There was an error transferring you to an agent.\"},\"Transitions\":{\"NextAction\":\"4b1c4159-1f57-4570-b96f-363f4a8132d4\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"MessageParticipant\"},{\"Identifier\":\"487aace6-4ffe-4a1d-8b1d-3d14ce447931\",\"Parameters\":{\"Text\":\"There is error getting your response\"},\"Transitions\":{\"NextAction\":\"4b1c4159-1f57-4570-b96f-363f4a8132d4\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"MessageParticipant\"},{\"Identifier\":\"78596bf3-a6bc-4efc-9741-44104789fb3e\",\"Parameters\":{\"Text\":\"There was an error transferring you to an agent.\"},\"Transitions\":{\"NextAction\":\"4b1c4159-1f57-4570-b96f-363f4a8132d4\",\"Errors\":[],\"Conditions\":[]},\"Type\":\"MessageParticipant\"},{\"Identifier\":\"4b1c4159-1f57-4570-b96f-363f4a8132d4\",\"Type\":\"DisconnectParticipant\",\"Parameters\":{},\"Transitions\":{}}]}",
    )

    ssm_client.put_parameter(
        Name='hlc302-flow-id',
        Value=response['ContactFlowId'],
        Type='String'
    )

    return response

@helper.update
def update(event, context):
    logger.info("Got Update")

@helper.delete
def delete(event, context):
    logger.info("Got Delete")

def lambda_handler(event, context):

    try:
        logger.info(f'event: {event}')

        helper(event, context)

    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)