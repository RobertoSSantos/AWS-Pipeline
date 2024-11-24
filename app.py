from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask running on Lambda!"

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": home()
    }