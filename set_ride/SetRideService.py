import boto3
import os


def set_ride(user, bus, stop, preset, agency):
    update_exp = 'SET #p = :b'
    user_table = boto3.resource('dynamodb').Table(os.environ['user_table'])
    response = user_table.update_item(
        Key={
            'user': user
        },
        UpdateExpression=update_exp,
        ExpressionAttributeNames={
            '#p': '%s-%s' % (agency, preset)
        },
        ExpressionAttributeValues={
            ':b': {'bus': bus, 'stop': stop}
        }
    )['ResponseMetadata']
    if response['HTTPStatusCode'] != 200:
        return 1
    else:
        return 0

if __name__ == '__main__':
    os.environ['user_table'] = 'EZRide_Users'
    set_ride('123', '7', '1174', '1', 'chicago-cta-bus')