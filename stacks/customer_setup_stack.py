import platform
from typing_extensions import runtime
from aws_cdk import core as cdk
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_ssm as ssm

class CustomerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if platform.system() == 'Windows':
            chat_sdk = 'lambdas\chat-sdk\ChatSDK.zip'
            chat_code = 'lambdas\start-chat'
        else:
            chat_sdk = 'lambdas/chat-sdk/ChatSDK.zip'
            chat_code = 'lambdas/start-chat'

        chat_sdk_layer = aws_lambda.LayerVersion(self,
            id='ChatSdkLayer',
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_7],
            compatible_architectures=[aws_lambda.Architecture.X86_64],
            description='The AWS SDK including Amazon Connect Chat APIs.',
            code=aws_lambda.Code.from_asset(chat_sdk)
        )

        start_chat_handler = aws_lambda.Function(self,
            id='StartChatLambda',
            code=aws_lambda.Code.from_asset(chat_code),
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler='startChatContact.lambda_handler',
            layers=[chat_sdk_layer],
            memory_size=128,
            timeout=cdk.Duration.seconds(30)
        )

        start_chat_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonConnect_FullAccess'
            )
        )

        start_chat_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonSSMFullAccess'
            )
        )

        apigw_iam_role = iam.Role(self,
            id='CustomerApiGwRole',
            assumed_by=iam.ServicePrincipal(
                service='apigateway.amazonaws.com'
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'service-role/AWSLambdaRole'
                )
            ]
        )

        customer_rest_api = apigw.RestApi(self,
            id='CustomerRestApi',
            rest_api_name='start-chat-contact',
            description='API to initiate chat with Amazon Connect'
        )

        response_model = apigw.Model(self,
            id='ApiGwResponseModel',
            rest_api=customer_rest_api,
            content_type='application/json',
            schema=({})
        )

        customer_rest_api.root.add_method(
            http_method='POST',
            api_key_required=False,
            authorization_type=apigw.AuthorizationType.NONE,
            integration=apigw.LambdaIntegration(
                handler=start_chat_handler,
                passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH
            ),
            method_responses=[
                apigw.MethodResponse(
                    status_code='200',
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                    response_models={
                        "application/json": response_model
                    }
                ),
                apigw.MethodResponse(
                    status_code='500',
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                    response_models={
                        "application/json": response_model
                    }
                )
            ]
        )

        customer_rest_api.root.add_method(
            http_method='OPTIONS',
            api_key_required=False,
            authorization_type=apigw.AuthorizationType.NONE,
            method_responses=[
                apigw.MethodResponse(
                    status_code='200',
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                    response_models={
                        "application/json": response_model
                    }
                )
            ],
            integration=apigw.Integration(
                type=apigw.IntegrationType.MOCK,
                options=apigw.IntegrationOptions(
                    passthrough_behavior=apigw.PassthroughBehavior.NEVER,
                    request_templates={
                        "application/json": '{"statusCode": 200}'
                    },
                    integration_responses=[
                        apigw.IntegrationResponse(
                            status_code='200',
                            response_parameters={
                                "method.response.header.Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                                "method.response.header.Access-Control-Allow-Methods": "''POST,OPTIONS''",
                                "method.response.header.Access-Control-Allow-Origin": "''*''"
                            },
                            response_templates={
                                "application/json": ""
                            }
                        )
                    ]
                )
            )
        )
        # Get latest version or specified version of plain string attribute
        connect_instance_alias = ssm.StringParameter.value_for_string_parameter(
            self, "hlc302-connect-instance-alias")
            
        connect_alias = cdk.CfnOutput(self,
            id='InstanceAlias',
            value=connect_instance_alias,
            export_name='AliasId'
        )

        api_gateway = cdk.CfnOutput(self,
            id='ApiGateway',
            value=customer_rest_api.url,
            export_name='CustomerApiGateway'
        )
