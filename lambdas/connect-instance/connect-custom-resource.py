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

# connect instance alias name
instance_alias = 'hlc302-testing1' # TODO CHANGE ME

@helper.create
def create(event, context):
    logger.info("Got Create")

    create_connect = connect_client.create_instance(
        IdentityManagementType='CONNECT_MANAGED',
        InstanceAlias=instance_alias,
        InboundCallsEnabled=True,
        OutboundCallsEnabled=True
    )

    ssm_client.put_parameter(
        Name='hlc302-connect-instance-id',
        Value=create_connect['Id'],
        Type='String'
    )

    time.sleep(75)

    return create_connect

@helper.update
def update(event, context):
    logger.info("Got Update")

    return 'Got Update'

@helper.delete
def delete(event, context):
    logger.info("Got Delete")

    connect_instance_id = ssm_client.get_parameter(
        Name='hlc302-connect-instance-id'
    )

    logger.info(connect_instance_id)

    delete_connect = connect_client.delete_instance(
        InstanceId=connect_instance_id['Parameter']['Value']
    )

    logger.info(delete_connect)

    delete_param = ssm_client.delete_parameter(
        Name='hlc302-connect-instance-id'
    )

    logger.info(delete_param)

    return delete_connect

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