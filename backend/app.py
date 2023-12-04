# backend/app.py

from flask import Flask, request, jsonify,render_template
import requests
import boto3

app = Flask(__name__)

def get_commits_count(username, repository, token):
    url = f"https://api.github.com/repos/{username}/{repository}/commits"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    commits = response.json()

    return len(commits)

def assess_productivity(commits_count, code_quality, response_time):
    # Define threshold values for each metric
    commit_threshold = 50  # Example: A developer is considered productive if they make at least 50 commits.
    code_quality_threshold = 80  # Example: Code quality is assessed on a scale of 0 to 100.
    response_time_threshold = 2  # Example: A response time of 2 hours or less is considered good.

    # Weighted scores for each metric
    commit_score = min(commits_count, commit_threshold) / commit_threshold * 100
    code_quality_score = code_quality / code_quality_threshold * 100
    response_time_score = max(0, 1 - response_time / response_time_threshold) * 100

    # Overall productivity score (you can adjust the weights based on your priorities)
    overall_score = 0.4 * commit_score + 0.4 * code_quality_score + 0.2 * response_time_score

    # Define a productivity threshold (adjust as needed)
    productivity_threshold = 70

    # Assess productivity based on the overall score
    if overall_score >= productivity_threshold:
        return "Productive"
    else:
        return "Not Productive"

def store_in_dynamodb(username, productivity_result,commits_count,code_quality, response_time):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace 'your-region' with your AWS region
    table = dynamodb.Table('ProductivityResults')  # Replace 'ProductivityResults' with your DynamoDB table name

    table.put_item(Item={
        'Username': username,
        'commits_count':commits_count,
        'code_quality':code_quality,
        'response_time':response_time,
        'ProductivityResult': productivity_result
    })
    
    #print("PutItem succeeded:", commits_count,code_quality, response_time)

@app.route('/api/productivity', methods=['POST'])
def get_productivity():
    data = request.json
    github_username = data["github_username"]
    github_repository = data["github_repository"]
    github_token = data["github_token"]

    commits_count = get_commits_count(github_username, github_repository, github_token)

    # For simplicity, code quality and response time are hardcoded. You may fetch these from additional APIs or databases.
    code_quality = 85
    response_time = 3  # Example: Response time in hours

    productivity_result = assess_productivity(commits_count, code_quality, response_time)

    # Store the result in DynamoDB
    store_in_dynamodb(github_username, productivity_result,commits_count,code_quality, response_time)

    return jsonify({"result": f"{github_username} is {productivity_result}"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
