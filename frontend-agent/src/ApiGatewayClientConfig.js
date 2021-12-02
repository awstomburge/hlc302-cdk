
import { INVOKE_URL, ACCESS_KEY, SECRET_KEY, AWS_REGION } from './AgentConfig';

const APIGatewayClientConfig = {
  invokeUrl: "https://1qm1tr0jb9.execute-api.us-east-1.amazonaws.com/prod/",
  accessKey: ACCESS_KEY,
  secretKey: SECRET_KEY,
  region: AWS_REGION
};

export default APIGatewayClientConfig;