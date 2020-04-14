def make_response(status_code, body):
    import json
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }