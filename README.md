
# HLC302 Reinvent Builders Session

Install NodeJS
Install Python <=3.7
Install CDK
Install AWS CLI

Configure AWS CLI profile with full access for Connect, Lex, and SSM at the minimum.

Create a python virtual env in project directory

cd hlc302
python -m venv hlc302
hlc302\Scripts\activate
pip list
Follow instructions to upgrade pip
pip install -r requirements.txt

cdk deploy --profile <aws cli profile name>