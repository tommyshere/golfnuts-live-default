import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
tournament_cache = dynamodb.Table("GolfNutsCache")
connections_table = dynamodb.Table("GolfNutsLiveConnections")

APIGW_ENDPOINT = os.getenv("APIGW_ENDPOINT")
apig_management_client = boto3.client("apigatewaymanagementapi", endpoint_url=APIGW_ENDPOINT)


def main(event, _):
    body = json.loads(event.get("body", "{}"))
    action = body.get("action")

    if action == "round-start":
        broadcast_message(body)

    return {"statusCode": 200, "body": json.dumps({"message": "Processed"})}


def broadcast_message(message):
    """Sends a WebSocket message to a specific client via API Gateway."""
    # Get all connection IDs from DynamoDB
    response = dynamodb.scan(TableName="GolfNutsLiveConnections")
    connection_ids = [item['connection_id']['S'] for item in response.get('Items', [])]

    for connection_id in connection_ids:
        try:
            apig_management_client.post_to_connection(
                Data=json.dumps(message).encode('utf-8'), ConnectionId=connection_id
            )
        except Exception as e:
            print(f"Failed to send message to {connection_id}: {e}")
