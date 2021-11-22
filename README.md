
# HLC302 Reinvent Builders Session

For this session, we will be building the following architecture:

![HLC302 architecture](images/architecture.png)

Install the following applications based on your system:
- [NodeJS](https://nodejs.org/en/download/)
        ```
        curl https://raw.github.com/creationix/nvm/master/install.sh | sh
        . ~/.bashrc
        nvm install 14.17.5
        nvm use 14.17.5
        nvm alias default v14.17.5
        ```
- [Python <=3.7](https://www.python.org/downloads/release/python-3614/)  
- [AWS CDK (`npm install aws-cdk -g`)](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Configure the CLI to have full access to Amazon Connect, Amazon Lex, and AWS Systems Manager. To make this easy, you can assign the user the CLI is using with Adminstrator permissions.

**NOTE: This solution is expecting you will run this in us-east-1**

Begin deploying the code:
- cd hlc302-cdk  
- Create a virtual environment for python: `python -m venv hlc302`
- To activate this environment:
  - If on Windows, run `hlc302\Scripts\activate`
  - If on Mac/Linux, run `source hlc302/bin/activate`
- Upgrade pip via `pip install --upgrade pip`
- Run `pip install -r requirements.txt`

If you've never deployed the AWS CDK before, you must first bootstrap it:
- `cdk bootstrap aws://<YOUR_ACCOUNT_ID>/<CURRENT_REGION>`

Once the bootstrap completes, deploy the code:
- `cdk deploy --all -O frontend-agent/src/cdk-outputs.json`

Once the deploy completes, follow the steps below. 
- Open **Amazon Connect** in the AWS Console. Click on the **Instance alias** for your instance. It will start with reinvent2021. 
  - From the left navigation, click on **Contact Flows**. Under the **Amazon Lex** section, select the Lambda function called `StartVideoCall(Classic)` in the **Bot** box. Click the button that says **+ Add Amazon Lex Bot**. 
  - From the left navigation, click on **Approved origins**. Click the **Add domain** button and enter `https://localhost:8080`. Click the **Add domain** button to save the change.
- Now click on the Amazon Connect **Access URL**. The username for the Connect instance can be found on line 24 of `lambdas\create-user\create-user-custom-resource.py`. The password is found on line 25 of that same file.
  - In the Amazon Connect console that appears, hover over the **Routing** icon and select **Contact flows**. 
  - On the screen that appears, click the **Create contact flow** button. 
  - Click the arrow at the upper right corner of the screen and select **Import flow (beta)**. 
  - In the box that appears, select `lambdas\import-flow\Chime Connect Integration flow.json`. Click **Import**. 
  - Click the **Save** button. Then click the **Publish** button. 
  - Under the contact flow name (top left side of the screen), click the **Show additional flow information** link. Copy the ID that appears in the ARN after `/contact-flow/`. For example, if your ARN is `arn:aws:connect:us-east-1:999999999999:instance/a1111111-1111-1111-1111-b11111111111/contact-flow/a1111111-b222-c3333-d4444-e55555555555`, you'll copy `a1111111-b222-c3333-d4444-e55555555555` for use in the next step. This value is the **Flow ID**.
  - Go to Systems Manager Parametere Store. Click the **Create parameter** button. 
  - In the **Name** field, enter `hlc302-flow-id`. In the value, enter the **Flow ID** from the previous step. Click the **Create parameter** button to save the value.

Install, build, and start frontend-agent  

```
cd frontend-agent  
npm install --force
npm run build  
npm run start  
```

Edit `frontend-customer\src\ConnectChatInterfaceConfig.js` with the proper values  
- The value for `API_GATEWAY_ENDPOINT` is found by looking at `frontend-agent/src/cdk-outputs.json`
- Navigate to Systems Manager and click on the **Parameter Store** tab. Click on the parameter called **hlc302-connect-instance-id**. The value you see is the value you should provide for the `INSTANCE_ID` variable. The value should have the pattern `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- The value for `CONTACT_FLOW_ID` is the **Flow ID** that you copied in saved in Parameter Store.

Install, build, and start frontend-customer  

```
cd frontend-customer  
npm install --force
npm run build  
npm run start  
```
