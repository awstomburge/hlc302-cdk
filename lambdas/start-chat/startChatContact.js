var AWS = require('aws-sdk');
AWS.config.update({region: process.env.REGION});
var connect = new AWS.Connect();
var SSM = new AWS.SSM();
​
exports.handler = async (event, context, callback) => {
    console.log("Received event: " + JSON.stringify(event));
    var body = JSON.parse(event["body"]);

    var responseFromSSM = await SSM.getParameter({"Name" : "hlc302-connect-instance-id"}).promise();
    var instance_id = responseFromSSM.Parameter.Value;
    console.log(instance_id);

    responseFromSSM = await SSM.getParameter({"Name" : "hlc302-flow-id"}).promise();
    var flow_parameter = responseFromSSM.Parameter.Value;
    console.log(flow_parameter);
​
    startChatContact(body, instance_id, flow_parameter).then((startChatResult) => {
        callback(null, buildSuccessfulResponse(startChatResult));
    }).catch((err) => {
        console.log("caught error " + err);
        callback(null, buildResponseFailed(err));
    });
};

function startChatContact(body, instanceId, contactFlowId) {

      return new Promise(function (resolve, reject) {
        var startChat = {
            "InstanceId": instanceId == "" ? process.env.INSTANCE_ID : instanceId,
            "ContactFlowId": contactFlowId == "" ? process.env.CONTACT_FLOW_ID : contactFlowId,
            "Attributes": {
                "customerName": body["ParticipantDetails"]["DisplayName"]
            },
            "ParticipantDetails": {
                "DisplayName": body["ParticipantDetails"]["DisplayName"]
            }
        };
​
        connect.startChatContact(startChat, function(err, data) {
            if (err) {
                console.log("Error starting the chat.");
                console.log(err, err.stack);
                reject(err);
            } else {
                console.log("Start chat succeeded with the response: " + JSON.stringify(data));
                resolve(data);
            }
        });
​    });
}

function buildSuccessfulResponse(result) {
    const response = {
        statusCode: 200,
        headers: {
            "Access-Control-Allow-Origin": "http://localhost:9000",
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials' : true,
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        },
        body: JSON.stringify({
            data: { startChatResult: result }
        })
    };
    console.log("RESPONSE" + JSON.stringify(response));
    return response;
}

function buildResponseFailed(err) {
    const response = {
        statusCode: 500,
        headers: {
            "Access-Control-Allow-Origin": "http://localhost:9000",
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials' : true,
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        },
        body: JSON.stringify({
            data: {
                "Error": err
            }
        })
    };
    return response;
}
