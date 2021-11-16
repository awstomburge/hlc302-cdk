from aws_cdk import core as cdk
from stacks.lex_bot_custom_resource import LexBotResource
from stacks.connect_custom_resource import ConnectInstanceResource
from stacks.associate_bot_custom_resource import AssociateBotResource
from stacks.import_flow_custom_resource import ImportFlowResource
from stacks.create_user_custom_resource import CreateUserResource

class CustomResourceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        lex_bot = LexBotResource(self, 'LB')

        connect_instance = ConnectInstanceResource(self, 'CI')

        associate_bot = AssociateBotResource(self, 'AB')
        associate_bot.node.add_dependency(lex_bot)
        associate_bot.node.add_dependency(connect_instance)

        import_flow = ImportFlowResource(self, 'IF')
        import_flow.node.add_dependency(connect_instance)

        create_user = CreateUserResource(self, 'CU')
        create_user.node.add_dependency(connect_instance)