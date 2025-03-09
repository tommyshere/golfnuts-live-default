import os
import requests
import json
import boto3
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth

dynamodb = boto3.resource("dynamodb")
tournament_cache = dynamodb.Table("GolfNutsCache")
connections_table = dynamodb.Table("GolfNutsLiveConnections")
APIGW_ENDPOINT = os.getenv("APIGW_ENDPOINT")

boto_session = boto3.session.Session()
credentials = boto_session.get_credentials()
region = boto_session.region_name


def main(event, _):
    connection_id = event["requestContext"]["connectionId"]
    body = json.loads(event.get("body", "{}"))
    action = body.get("action")
    tournament_id = body.get("tournamentId")

    if not tournament_id:
        return {"statusCode": 400, "body": json.dumps({"message": "Missing tournamentId"})}

    if action == "get_round_start_status":
        round_status = fetch_round_start_status(tournament_id)
        send_websocket_message(connection_id, round_status)

    return {"statusCode": 200, "body": json.dumps({"message": "Processed"})}


def fetch_round_start_status(tournament_id):
    """Returns whether a specific tournament round has started"""
    # Mock data — Replace with actual database query
    if tournament_id == "123":
        return {"tournamentId": tournament_id, "roundStarted": True}
    else:
        return {"tournamentId": tournament_id, "roundStarted": False}


def send_websocket_message(connection_id, message):
    """Sends a WebSocket message to a specific client via API Gateway."""
    url = f"{APIGW_ENDPOINT}/{connection_id}"
    request = AWSRequest(method="POST", url=url, data=json.dumps(message))

    SigV4Auth(credentials, "execute-api", region).add_auth(request)

    session = requests.Session()
    prepared_request = request.prepare()
    response = session.send(prepared_request)

    if response.status_code == 200:
        print(f"Message sent to {connection_id}")
    else:
        print(f"Failed to send message to {connection_id}: {response.text}")