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

# user info
user_name = 'admin'
user_password = 'AdminPassword1!'
user_first = 'Admin'
user_last = 'User'
user_email = 'admin@example.com'

@helper.create
def create(event, context):
    logger.info("Got Create")

    connect_instance_id = ssm_client.get_parameter(
        Name='hlc302-connect-instance-id'
    )

    security_profiles = connect_client.list_security_profiles(
        InstanceId=connect_instance_id['Parameter']['Value']
    )

    routing_profiles = connect_client.list_routing_profiles(
        InstanceId=connect_instance_id['Parameter']['Value']
    )

    admin_profile = ''
    routing_profile = ''

    for profile in security_profiles['SecurityProfileSummaryList']:
        if profile['Name'] == 'Admin':
            logger.info('Found Admin')
            logger.info(profile['Id'])
            admin_profile = profile['Id']

    for profile in routing_profiles['RoutingProfileSummaryList']:
        if profile['Name'] == 'Basic Routing Profile':
            logger.info('Found Routing Profile')
            logger.info(profile['Id'])
            routing_profile = profile['Id']

    create_user = connect_client.create_user(
        Username=user_name,
        Password=user_password,
        IdentityInfo={
            'FirstName': user_first,
            'LastName': user_last,
            'Email': user_email
        },
        PhoneConfig={
            'PhoneType': 'SOFT_PHONE',
        },
        SecurityProfileIds=[
            admin_profile,
        ],
        RoutingProfileId=routing_profile,
        InstanceId=connect_instance_id['Parameter']['Value']
    )

    logger.info(create_user)

    return create_user

@helper.update
def update(event, context):
    logger.info("Got Update")

    return 'Got Update'

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