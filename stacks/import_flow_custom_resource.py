from aws_cdk import core as cdk
from aws_cdk.custom_resources import Provider
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class ImportFlowResource(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        import_flow_handler = aws_lambda.Function(self,
            id='ImportFlowLambda',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            code=aws_lambda.Code.from_asset('lambdas\import-flow'),
            handler='import-flow-custom-resource.lambda_handler',
            timeout=cdk.Duration.seconds(90)
        )

        import_flow_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonConnect_FullAccess'
            )
        )

        import_flow_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        provider = Provider(self,
            id='ImportFlowResourceProvider',
            on_event_handler=import_flow_handler
        )

        import_flow_resource = cdk.CustomResource(self,
            id='ImportFlowResource',
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type='Custom::ImportFlow'
        )