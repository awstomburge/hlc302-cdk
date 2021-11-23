import platform
from aws_cdk import core as cdk
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda

class AgentStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if platform.system() == 'Windows':
            create_code = 'lambdas\create-chime-meeting'
            delete_code = 'lambdas\delete-chime-meeting'
        else:
            create_code = 'lambdas/create-chime-meeting'
            delete_code = 'lambdas/delete-chime-meeting'

        create_chime_meeting_handler = aws_lambda.Function(self,
            id='CreateChimeMeetingLambda',
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            code=aws_lambda.Code.from_asset(create_code),
            handler='index.handler',
            timeout=cdk.Duration.seconds(90)
        )

        create_chime_meeting_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonChimeSDK'
            )
        )

        delete_chime_meeting_handler = aws_lambda.Function(self,
            id='DeleteChimeMeetingLambda',
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            code=aws_lambda.Code.from_asset(delete_code),
            handler='index.handler',
            timeout=cdk.Duration.seconds(90)
        )

        delete_chime_meeting_handler.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonChimeSDK'
            )
        )

        apigw_iam_role = iam.Role(self,
            id='AgentApiGwRole',
            assumed_by=iam.ServicePrincipal(
                service='apigateway.amazonaws.com'
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'service-role/AWSLambdaRole'
                )
            ]
        )

        agent_rest_api = apigw.RestApi(self, 
            id='AgentRestApi',
            api_key_source_type=apigw.ApiKeySourceType.HEADER,
            endpoint_configuration=apigw.EndpointConfiguration(
                types=[apigw.EndpointType.EDGE]
            ),
            rest_api_name='chime-meeting-operations',
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=apigw.Cors.DEFAULT_HEADERS
            )
        )

        meeting = agent_rest_api.root.add_resource('meeting')

        response_model = apigw.Model(self,
            id='ApiGwResponseModel',
            rest_api=agent_rest_api,
            content_type='application/json',
            schema=({})
        )

        meeting.add_method(
            http_method='POST',
            api_key_required=False,
            authorization_type=apigw.AuthorizationType.IAM,
            method_responses=[
                apigw.MethodResponse(
                    status_code='200',
                    response_models={
                        "application/json": response_model
                    },
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    }
                )
            ],
            integration=apigw.LambdaIntegration(
                credentials_role=apigw_iam_role,
                integration_responses=[
                    apigw.IntegrationResponse(
                        status_code='200'
                    )
                ],
                passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH,
                proxy=True,
                handler=create_chime_meeting_handler
            )
        )

        meeting.add_method(
            http_method='DELETE',
            api_key_required=False,
            authorization_type=apigw.AuthorizationType.IAM,
            request_parameters={
                "method.request.querystring.meetingId": True
            },
            method_responses=[
                apigw.MethodResponse(
                    status_code='200',
                    response_models={
                        "application/json": response_model
                    },
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    }
                )
            ],
            integration=apigw.LambdaIntegration(
                credentials_role=apigw_iam_role,
                integration_responses=[
                    apigw.IntegrationResponse(
                        status_code='200'
                    )
                ],
                passthrough_behavior=apigw.PassthroughBehavior.WHEN_NO_MATCH,
                proxy=True,
                handler=delete_chime_meeting_handler
            )
        )

        chime_demo_user = iam.User(self,
            id='ChimeDemoUser',
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonAPIGatewayInvokeFullAccess'
                )
            ]
        )

        chime_demo_user_keys = iam.CfnAccessKey(self,
            id='ChimeDemoUserKeys',
            user_name=chime_demo_user.user_name,
            status='Active'
        )
            
        chime_demo_user_access = cdk.CfnOutput(self,
            id='ChimeDemoUserAccessKey',
            value=chime_demo_user_keys.ref,
            export_name='ChimeConnectDemoUserAccessKey'
        )

        chime_demo_user_secret = cdk.CfnOutput(self,
            id='ChimeDemoUserSecretKey',
            value=chime_demo_user_keys.attr_secret_access_key,
            export_name='ChimeConnectDemoUserSecretKey'
        )
        
        api_gateway = cdk.CfnOutput(self,
            id='ApiGateway',
            value=agent_rest_api.url,
            export_name='AgtApiGateway'
        )
        
        chime_region = cdk.CfnOutput(self,
            id='Region',
            value=self.region,
            export_name='Region'
        )
