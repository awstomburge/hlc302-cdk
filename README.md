
# HLC302 Reinvent Builders Session

Install the following applications based on your system:
- NodeJS  
- Python <=3.7  
- AWS CDK (`npm install -g aws-cdk`)  
- AWS CLI. Configure the CLI to have full access to Amazon Connect, Amazon Lex, ans AWS Systems Manager. To make this easy, you can assign the user the CLI is using with Adminstrator permissions.

Begin deploying the code:
- cd hlc302-cdk  
- Create a virtual environment for python: `python -m venv hlc302`
- To activate this environment:
  - If on Windows, run `hlc302\Scripts\activate`
  - If on Mac/Linux, run `source hlc302/bin/activate`
- Upgrade pip via `pip install --upgrade pip`
- Run `pip install -r requirements.txt`
- Edit line 24 of lambdas\connect-instance\connect-custom-resource.py. Change the Amazon Connect alias to be something unique. 

If you've never deployed the AWS CDK before, you must first bootstrap it:
- `cdk bootstrap aws://<YOUR_ACCOUNT_ID>/<CURRENT_REGION>`

Once the bootstrap completes, deploy the code:
- `cdk deploy --all --profile <AWS_PROFILE_NAME`

Once the deploy completes, edit `frontend-agent\src\AgentConfig.js` with the proper values. 
- The value for the `<INSTANCE-ALIAS>` is the value you entered for the Amazon Connect alias
- The values for the `INVOKE_URL`, `ACCESS_KEY`, and `SECRET_KEY` are most easily seen by navigating to the CloudFormation console and looking at the **Outputs** tab for the **hlc302-agent** stack

Edit `frontend-customer\src\ConnectChatInterfaceConfig.js` with the proper values  
- The value for `API_GATEWAY_ENDPOINT` is found by looking at the **Outputs** tab for the **hlc302-customer** stack
- Navigate to Systems Manager and click on the **Parameter Store** tab. Click on the parameter called **hlc302-connect-instance-id**. The value you see is the value you should provide for the `INSTANCE_ID` variable. The value should have the pattern `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- Find the parameter called **hlc302--tbd**. The value of this should be the value for the `CONTACT_FLOW_ID` variable.


install, build, and start frontend-agent  

cd frontend-agent  
npm install --force
npm run build  
npm run start  

install, build, and start frontend-customer  

cd frontend-customer  
npm install --force
npm run build  
npm run start  
