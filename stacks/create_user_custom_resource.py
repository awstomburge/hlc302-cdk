import platform
from aws_cdk import core as cdk
from aws_cdk.custom_resources import Provider
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class CreateUserResource(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        if platform.system() == 'Windows':
            user_code = 'lambdas\create-user'
        else:
            user_code = 'lambdas/create-user'

        create_user_handler = aws_lambda.Function(self,
            id='CreateUserLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset(user_code),
            handler='create-user-custom-resource.lambda_handler',
            timeout=cdk.Duration.seconds(90)
        )

        create_user_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonConnect_FullAccess'
            )
        )

        create_user_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        provider = Provider(self,
            id='CreateUserResourceProvider',
            on_event_handler=create_user_handler
        )

        create_user_resource = cdk.CustomResource(self,
            id='CreateUserResource',
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type='Custom::CreateConnectUser'
        )