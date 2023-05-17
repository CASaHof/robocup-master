from src import normalizePositions

cam1 = [
    {
        "x": 0.51,
        "y": 0.5,
    },
    {
        "x": 0.5,
        "y": 0.65
    }
]

cam2 = [
    {
        "x": 0.5,
        "y": 0.55
    },
    {
        "x": 0.5,
        "y": 0.3,
    }
]

if __name__=="__main__":
    robots = normalizePositions(cam1,cam2)
    print(robots)