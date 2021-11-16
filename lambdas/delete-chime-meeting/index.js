const AWS = require('aws-sdk');
const chime = new AWS.Chime({region: 'us-east-1'});
chime.endpoint = new AWS.Endpoint('https://service.chime.aws.amazon.com/console');

exports.handler = async (event, context, callback) => {
  let meetingInfo = null, result = null;
  const meetingId = event['queryStringParameters']['meetingId'];
  console.log("MeetingId: ", meetingId);
  let response = {
      statusCode: 200,
      body: 'meeting not available',
      headers:{ 'Access-Control-Allow-Origin' : '*' },
  };
  try {
    result = await chime.getMeeting({
      MeetingId: meetingId
    }).promise();
    console.log("Response after successfully getting the meeting:", result);
    if(result) {
      // meeting does exist
      meetingInfo = result;
    }
  } catch(err) {
    console.log("Error while checking chime:getMeeting", err);
  }

  if(meetingInfo) {
    try {
      result = await chime.deleteMeeting({
        MeetingId: meetingInfo.Meeting.MeetingId,
      }).promise();
      console.log("Result after deleteMeeting:", result);
      response.body = 'meeting deleted successfully';
    } catch(err) {
      console.log("Error while deleting meeting chime:deleteMeeting", err);
    }
  }

  return response;
};
