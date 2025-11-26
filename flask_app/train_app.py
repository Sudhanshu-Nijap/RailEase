from flask import Flask, request, render_template
import requests

app = Flask(__name__)

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

        return render_template('train_schedule.html', schedule=data['Route'])
    except Exception as e:
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

