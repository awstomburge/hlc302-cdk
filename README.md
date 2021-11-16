
# HLC302 Reinvent Builders Session

Install NodeJS  
Install Python <=3.7  
Install CDK  
Install AWS CLI  

Configure AWS CLI profile with full access for Connect, Lex, and SSM at the minimum.  

Create a python virtual env in project directory.  

cd hlc302  
python -m venv hlc302  
hlc302\Scripts\activate  
pip list  
Follow instructions to upgrade pip  
pip install -r requirements.txt  

edit lambdas\connect-instance\connect-custom-resource.py on line 24 to change the Connect alias

cdk deploy --profile <aws cli profile name>

edit frontend-agent\src\AgentConfig.js with the proper values  

edit frontend-customer\src\ConnectChatInterfaceConfig.js with the proper values  

install, build, and start frontend-agent  

npm install  
npm run build  
npm run start  

install, build, and start frontend-customer  

npm install  
npm run build  
npm run start  
