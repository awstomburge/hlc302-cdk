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

    with open('chime-connect-integration-flow.json', 'r') as json_file:
        data = json.loads(json_file.read())

    response = connect_client.create_contact_flow(
        InstanceId=connect_instance_id['Parameter']['Value'],
        Name='Chime Connect Integration flow',
        Type='CONTACT_FLOW',
        Content=json.dumps(data)
    )

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