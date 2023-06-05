# Cooperative Autonomous Driving - Robocup Master

The goal is to detect [NAO6](https://www.aldebaran.com/en/support/nao-6) robots inside a soccer field.

For that we use [YOLOv8](https://github.com/ultralytics/ultralytics) to detect those within a python 3.9 environment.

We use one cameras on each side so calculate the positions for that.

# Effective field size:

4.5m x 2.5m

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

# Web Server

[GET] `/` \
_Shows the live dashboard._

[GET] `/res/*.png` \
_Loads a .png inside the [Ressources](src/web/res) Folder._

[GET] `/res/*.jpg` \
_Loads a .jpg inside the [Ressources](src/web/res) Folder._

# Example Message

We will serve a websocket server for the team server to connect to where we will publish the following object:

```json
{
  "state": "string",
  "time_remaining": "number",
  "teams": [
    {
      "name": "string",
      "score": "number"
    },
    {
      "name": "string",
      "score": "number"
    }
  ],
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
      "y": "number"
    }
  ]
}
```

The `state` can be one of the following: `playing`, `paused`, `foul`, `ended`, `goal`.

The `time_remaining` is an integer of the remaining seconds to play.

## Übersicht Spielfeld

![Alt text](images/top%20down.png)

## Exemplarische Ansicht der Kamera

![Alt text](images/empty%20field.png)

![Alt text](images/field.png)
