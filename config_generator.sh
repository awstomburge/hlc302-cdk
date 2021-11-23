sudo yum install jq -y
api_endpoint=$(jq -r .hlc302Customer.ApiGateway ./frontend-agent/src/cdk-outputs.json )
region=$(jq -r .hlc302Agent.Region ./frontend-agent/src/cdk-outputs.json )
instance_id=$(aws ssm get-parameter --name "hlc302-connect-instance-id" --with-decryption --output text --query Parameter.Value)
flow_id=$(aws ssm get-parameter --name "hlc302-flow-id" --with-decryption --output text --query Parameter.Value)
touch ./frontend-customer/src/script-outputs.json
echo -e "{
\"region\":\"$region\",
\"api_endpoint\":\"$api_endpoint\",
\"instance_id\":\"$instance_id\",
\"flow_id\": \"$flow_id\"
}" > ./frontend-customer/src/script-outputs.json