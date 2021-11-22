import cdkExports from './cdk-outputs.json';

export const AGENT_CCP_URL = 'https://' + cdkExports.hlc302Customer.InstanceId + '.my.connect.aws/connect/ccp-v2/chat';

export const AWS_REGION = cdkExports.hlc302Agent.Region;

// Check the invokeURL under the ChimeConnectIntegrationDemo CF template output tab
export const INVOKE_URL = cdkExports.hlc302Agent.ApiGateway;

// Check the ChimeConnectDemoUserAccessKey under the ChimeConnectIntegrationDemo CF template output tab
export const ACCESS_KEY = cdkExports.hlc302Agent.ChimeDemoUserAccessKey;

// Check the ChimeConnectDemoUserSecretKey under the ChimeConnectIntegrationDemo CF template output tab 
export const SECRET_KEY = cdkExports.hlc302Agent.ChimeDemoUserSecretKey;