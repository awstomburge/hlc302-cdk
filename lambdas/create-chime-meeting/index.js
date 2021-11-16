// function to create a unique id
function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// require AWS SDK
const AWS = require('aws-sdk');

// Create the new AWS Chime object in the 'us-east-1' region
const chime = new AWS.Chime({region: 'us-east-1'});

// Create and attach the AWS service endpoint for chime
chime.endpoint = new AWS.Endpoint('https://service.chime.aws.amazon.com/console');

let request = null, agentAttendee = null, customerAttendee = null;

// lambda handler
exports.handler = async (event, context, callback) => {
    let meeting = null;

    // create a unique request id
    const requestId = uuid();

    // specify media placement region
    const region = 'us-east-1';

    // prepare the request for creating the chime meeting
    request = {
      ClientRequestToken: requestId,
      MediaRegion: region,
    };
    try {
      // create chime meeting
      meeting = await chime.createMeeting(request).promise();
    } catch (err) {
      console.log("Some error occured in creating the meeting", err);
    }

    // create attendees -> agent and customer
    if(meeting) {
      console.log("Created Meeting with id:", meeting.Meeting.MeetingId);

      // create the agent attendee creation request
      request = {
        MeetingId: meeting.Meeting.MeetingId,
        ExternalUserId: uuid()
      };
      agentAttendee = null;
      try {
        // create agent attendee
        agentAttendee = await chime.createAttendee(request).promise();
        console.log("Agent attendee created with id:", agentAttendee.Attendee.AttendeeId);
      } catch (err) {
        console.log("Some error occured in creating the agent as attendee", err);
      }

      // create the customer attendee creation request
      if(agentAttendee) {
        request = {
          MeetingId: meeting.Meeting.MeetingId,
          ExternalUserId: uuid()
        };
        customerAttendee = null;
        try {
          // create customer attendee
          customerAttendee = await chime.createAttendee(request).promise();
          console.log("Customer attendee created with id:", customerAttendee.Attendee.AttendeeId);
        } catch (err) {
          console.log("Some error occured in creating the customer as attendee", err);
        }
      }
    }

    let response = {
      statusCode: 500,
      body: 'Internal error occured, check lambda execution logs',
    };

    // once the meeting is created with agent and customer as attendees send this response
    if( meeting && agentAttendee && customerAttendee ) {
      const joinInfo = {
        "meeting": meeting,
        "agentAttendee": agentAttendee,
        "customerAttendee": customerAttendee
      };
      response = {
        "statusCode": 200,
        'headers': {
          "Access-Control-Allow-Origin": "*"
        },
        "body": JSON.stringify(joinInfo)
      };
    }

    callback(null, response);
};
