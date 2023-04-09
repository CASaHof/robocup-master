"# cas-robocup-master" 
# Cooperative Autonomous Driving - Robocup Master

The goal is to detect [NAO6](https://www.aldebaran.com/en/support/nao-6) robots inside a soccer field.

For that we use [YOLOv8](https://github.com/ultralytics/ultralytics) to detect those within a python 3.9 environment.

We use one cameras on each side so calculate the positions for that.

# Installation

## Windows
```bash
copy .env.example .env
pip install -r requirements.txt
```

## Unix
```bash
cp .env.example .env
pip install -r requirements.txt
```

# Usage
```bash
python server.py
```

# Example Message

We will serve a websocket server for the team server to connect to where we will publish the following object:

```json
{
    "state": "string",
    "time_remaining": "number",
    "robots": [
        {
            "x": "number",
            "y": "number",
            "id": "UUID",
            "angle": "number"
        }
    ],
    "balls": [
        {
            "x": "number",
            "y": "number",
        }   
    ]
}
```

