
# HLC302 Reinvent Builders Session

Install the following applications based on your system:
- [NodeJS](https://nodejs.org/en/download/)
- [Python <=3.7](https://www.python.org/downloads/release/python-3614/)  
- [AWS CDK (`npm install -g aws-cdk`)](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Configure the CLI to have full access to Amazon Connect, Amazon Lex, and AWS Systems Manager. To make this easy, you can assign the user the CLI is using with Adminstrator permissions.

Begin deploying the code:
- cd hlc302-cdk  
- Create a virtual environment for python: `python -m venv hlc302`
- To activate this environment:
  - If on Windows, run `hlc302\Scripts\activate`
  - If on Mac/Linux, run `source hlc302/bin/activate`
- Upgrade pip via `pip install --upgrade pip`
- Run `pip install -r requirements.txt`
- Edit line 24 of `lambdas\connect-instance\connect-custom-resource.py`. Change the Amazon Connect alias to be something unique. **If you don't make this change, your install will fail**.

If you've never deployed the AWS CDK before, you must first bootstrap it:
- `cdk bootstrap aws://<YOUR_ACCOUNT_ID>/<CURRENT_REGION>`

Once the bootstrap completes, deploy the code:
- `cdk deploy --all --profile <AWS_PROFILE_NAME>`

Once the deploy completes, edit `frontend-agent\src\AgentConfig.js` with the proper values. 
- The value for the `<INSTANCE-ALIAS>` is the value you entered for the Amazon Connect alias
- The values for the `INVOKE_URL`, `ACCESS_KEY`, and `SECRET_KEY` are most easily seen by navigating to the CloudFormation console and looking at the **Outputs** tab for the **hlc302-agent** stack

Install, build, and start frontend-agent  

```
cd frontend-agent  
npm install --force
npm run build  
npm run start  
```

Edit `frontend-customer\src\ConnectChatInterfaceConfig.js` with the proper values  
- The value for `API_GATEWAY_ENDPOINT` is found by looking at the **Outputs** tab for the **hlc302-customer** stack
- Navigate to Systems Manager and click on the **Parameter Store** tab. Click on the parameter called **hlc302-connect-instance-id**. The value you see is the value you should provide for the `INSTANCE_ID` variable. The value should have the pattern `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- `CONTACT_FLOW_ID` - **TBD**.

Install, build, and start frontend-customer  

```
cd frontend-customer  
npm install --force
npm run build  
npm run start  
```