import boto3
from mypy_boto3_dynamodb.service_resource import Table
from pydantic import BaseModel


class EventIntercepted(BaseModel):
    metadata: str
    receipt_id: str
    data: str


def get_event_from_table(table_name: str, event_source: str, event_name: str, receipt_id: str) -> EventIntercepted:
    """Fetch event intercepted and stored in DynamoDB table.

    Intercepted events are stored with a primary key named: {event_source}#{event_name}#{receipt_id}.

    This helps prevent data concurrency issues like parallel tests, shared stacks, or partial test failures.

    Pros:

    - Receipt ID is known at ingestion time allowing us to guarantee a single match
    - Event source is named after the test name allowing full traceability (e.g., test_event_bridge_provider_send)

    Cons:

    - Testing a batch of events is inefficient with this function (N calls)

    Parameters
    ----------
    table_name : str
        Table name with events intercepted
    event_source
        Event source for event intercepted
    event_name
        Event name
    receipt_id
        Receipt ID for event ingested earlier

    Returns
    -------
    EventIntercepted
        Event intercepted and retrieved from DynamoDB table
    """
    pk = f'{event_source}#{event_name}#{receipt_id}'

    ddb = boto3.resource('dynamodb')
    table: Table = ddb.Table(table_name)
    ret = table.query(KeyConditionExpression='pk = :pk', ExpressionAttributeValues={':pk': pk})

    item = ret['Items'][0]  # todo: allow multiple events to be batched
    return EventIntercepted(metadata=item['metadata'], data=item['data'], receipt_id=item['receipt_id'])  # type: ignore[arg-type]
