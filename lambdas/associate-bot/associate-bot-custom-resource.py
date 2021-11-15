# standard imports
import os, sys, logging, traceback, json

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

# get region
region = os.environ['AWS_REGION']

logger.info(region)

@helper.create
def create(event, context):
    logger.info("Got Create")

    bot_name = ssm_client.get_parameter(
        Name='hlc302-lex-bot-name'
    )

    logger.info(bot_name)

    connect_instance_id = ssm_client.get_parameter(
        Name='hlc302-connect-instance-id'
    )

    logger.info(connect_instance_id)

    bot = {
            'Name': bot_name['Parameter']['Value'],
            'LexRegion': region
    }

    logger.info(bot)

    associate_bot = connect_client.associate_bot(
        InstanceId=connect_instance_id['Parameter']['Value'],
        LexBot=bot
    )

    logger.info(associate_bot)

    return associate_bot

@helper.update
def update(event, context):
    logger.info("Got Update")

    return 'Got Update'

@helper.delete
def delete(event, context):
    logger.info("Got Delete")

    return 'Got Delete'

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