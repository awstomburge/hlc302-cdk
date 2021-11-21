import platform
from aws_cdk import core as cdk
from aws_cdk.custom_resources import Provider
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class ConnectInstanceResource(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        if platform.system() == 'Windows':
            connect_code = 'lambdas\connect-instance'
        else:
            connect_code = 'lambdas/connect-instance'

        connect_instance_handler = aws_lambda.Function(self,
            id='ConnectInstanceLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset(connect_code),
            handler='connect-custom-resource.lambda_handler',
            timeout=cdk.Duration.seconds(125)
        )

        connect_instance_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonConnect_FullAccess'
            )
        )

        connect_instance_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        provider = Provider(self,
            id='ConnectInstanceResourceProvider',
            on_event_handler=connect_instance_handler
        )

        connect_instance_resource = cdk.CustomResource(self,
            id='ConnectInstanceResource',
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type='Custom::ConnectInstance'
        )
