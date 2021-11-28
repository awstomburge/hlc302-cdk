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
lex_client = boto3.client('lex-models')
ssm_client = boto3.client('ssm')

# bot name
bot_name = 'StartVideoCall'

@helper.create
def create(event, context):
    logger.info("Got Create")

    # lex_client.put_intent(name='Chat', sampleUtterances=['Chat'], fulfillmentActivity={'type':'ReturnIntent'})
    # lex_client.create_intent_version(name='Chat')
    
    # lex_client.put_intent(name='Video', sampleUtterances=['Video'], fulfillmentActivity={'type':'ReturnIntent'})
    # lex_client.create_intent_version(name='Video')

    create_bot = lex_client.put_bot(
        name=bot_name,
        intents=[
            {
                'intentName': 'Chat',
                'intentVersion': '1'
            },
            {
                'intentName': 'Video',
                'intentVersion': '1'
            }
        ],
        voiceId='0',
        childDirected=False,
        locale='en-US',
        idleSessionTTLInSeconds=3600,
        clarificationPrompt={
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Sorry, can you please repeat that?'
                }
            ],
            'maxAttempts': 5
        },
        abortStatement={
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Sorry, I could not understand. Goodbye.'
                }
            ]
        },
        detectSentiment=False,
        createVersion=True
    )

    logger.info(create_bot)

    ssm_client.put_parameter(
        Name='hlc302-lex-bot-name',
        Value=bot_name,
        Type='String'
    )

    time.sleep(30)

    return create_bot

@helper.update
def update(event, context):
    logger.info("Got Update")

@helper.delete
def delete(event, context):
    logger.info("Got Delete")

    bot_param = ssm_client.get_parameter(
        Name='hlc302-lex-bot-name'
    )

    delete_bot = lex_client.delete_bot(
        name=bot_param['Parameter']['Value']
    )

    logger.info(delete_bot)

    delete_param = ssm_client.delete_parameter(
        Name='hlc302-lex-bot-name'
    )

    logger.info(delete_param)

    return delete_bot

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