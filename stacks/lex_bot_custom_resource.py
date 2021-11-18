import platform
from aws_cdk import core as cdk
from aws_cdk.custom_resources import Provider
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class LexBotResource(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        if platform.system() == 'Windows':
            bot_code = 'lambdas\lex-bot'
        else:
            bot_code = 'lambdas/lex-bot'

        lex_bot_handler = aws_lambda.Function(self,
            id='LexBotLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset(bot_code),
            handler='lex-bot-custom-resource.lambda_handler',
            timeout=cdk.Duration.seconds(90)
        )

        lex_bot_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonLexFullAccess'
            )
        )

        lex_bot_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        provider = Provider(self,
            id='LexBotResourceProvider',
            on_event_handler=lex_bot_handler
        )

        lex_box_resource = cdk.CustomResource(self,
            id='LexBotResource',
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type='Custom::LexBot'
        )