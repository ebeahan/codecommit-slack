import boto3
import json
import os
import requests

codecommit = boto3.client('codecommit')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

def lambda_handler(event, context):
    # Parse repo and commit info from response event payload
    repository = event['Records'][0]['eventSourceARN'].split(':')[5]
    commit_id = event['Records'][0]['codecommit']['references'][0]['commit']
    branch = event['Records'][0]['codecommit']['references'][0]['ref'].split('/')[-1]
    # Retrieve information with the provided git commit hash
    commit_info = codecommit.get_commit(repositoryName=repository, commitId=commit_id)
    print(commit_info)
    # shorten for slack output
    commit_id_short = commit_id[-8:-1]
    commit_author = commit_info['commit']['author']['name']
    commit_message = commit_info['commit']['message']

    # Format slack data
    slack_data = {
        "attachments": [
            {
                "color": "#36a64f",
                "pretext": "[{}/{}] New commit pushed by {}".format(repository, branch, commit_author),
                "text": "`{}` {}".format(commit_id_short, commit_message, commit_author),
                "username": "CodeCommit Bot",
                "mrkdwn": True
            }
        ]
    }

    # Post data to slack webhook url
    response = requests.post(
        SLACK_WEBHOOK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
