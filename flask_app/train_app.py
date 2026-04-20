from flask import Flask, request, render_template, redirect, url_for
import requests
import boto3
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# AWS DynamoDB Config
db_available = False
table = None

try:
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    TABLE_NAME = 'RailEaseSearchHistory'
    table = dynamodb.Table(TABLE_NAME)
    # Check connection if keys are present
    if os.getenv('AWS_ACCESS_KEY_ID'):
        table.table_status
        db_available = True
except Exception as e:
    print(f"DynamoDB not available (History feature disabled): {e}")

def save_search(train_no, search_type):
    if not db_available or table is None:
        return
    try:
        table.put_item(
            Item={
                'search_id': str(uuid.uuid4()),
                'train_no': train_no,
                'search_type': search_type,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")

API_KEY = "bb89dd4cde5bd8e1ac6e12f000b4fea1"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train_info', methods=['GET'])
def train_info():
    train_no = request.args.get('train_no')
    if not train_no:
        return render_template('error.html', message="Please provide a train number.")
    try:
        response = requests.get(f"https://indianrailapi.com/api/v2/TrainInformation/apikey/{API_KEY}/TrainNumber/{train_no}")
        data = response.json()

        if "TrainName" not in data:
            return render_template('error.html', message="Invalid train number or API error.")

        save_search(train_no, "Information")

        return render_template('train_info.html', 
                               train_name=data['TrainName'], 
                               source_code=data['Source']['Code'], 
                               source_arrival=data['Source']['Arrival'], 
                               destination_code=data['Destination']['Code'], 
                               destination_arrival=data['Destination']['Arrival'])
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/train_schedule', methods=['GET'])
def train_schedule():
    train_no = request.args.get('train_no')
    if not train_no:
        return render_template('error.html', message="Please provide a train number.")
    try:
        response = requests.get(f"https://indianrailapi.com/api/v2/TrainSchedule/apikey/{API_KEY}/TrainNumber/{train_no}")
        data = response.json()

        if "Route" not in data:
            return render_template('error.html', message="Invalid train number or API error.")

        save_search(train_no, "Schedule")

        return render_template('train_schedule.html', schedule=data['Route'])
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/history')
def history():
    if not db_available:
        return render_template('history.html', history=[], db_error="Search history is currently unavailable (AWS credentials missing).")
    try:
        response = table.scan()
        items = response.get('Items', [])
        # Sort by timestamp descending
        items.sort(key=lambda x: x['timestamp'], reverse=True)
        return render_template('history.html', history=items[:20])
    except Exception as e:
        return render_template('history.html', history=[], db_error=f"Could not load history: {e}")

if __name__ == '__main__':
    app.run(debug=True)
