from aws_cdk import core as cdk
from aws_cdk.custom_resources import Provider
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class AssociateBotResource(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        associate_bot_handler = aws_lambda.Function(self,
            id='AssociateBotLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset('lambdas\\associate-bot'),
            handler='associate-bot-custom-resource.lambda_handler',
            timeout=cdk.Duration.seconds(90)
        )

        associate_bot_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonConnect_FullAccess'
            )
        )

        associate_bot_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonLexFullAccess'
            )
        )

        associate_bot_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        provider = Provider(self,
            id='AssociateBotResourceProvider',
            on_event_handler=associate_bot_handler
        )

        associate_bot_resource = cdk.CustomResource(self,
            id='AssociateBotResource',
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type='Custom::AssociateBot'
        )