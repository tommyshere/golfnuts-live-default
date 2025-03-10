import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
tournament_cache = dynamodb.Table("GolfNutsCache")
connections_table = dynamodb.Table("GolfNutsLiveConnections")

APIGW_ENDPOINT = os.getenv("APIGW_ENDPOINT")
apig_management_client = boto3.client("apigatewaymanagementapi", endpoint_url=APIGW_ENDPOINT)


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
    send_response = apig_management_client.post_to_connection(
        Data=json.dumps(message).encode('utf-8'), ConnectionId=connection_id
    )
    print(send_response)
