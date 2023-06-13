def nPos(pos:float,target:float,offset:float=0.05):
    # print(f"pos={pos} target={target} offset={offset}")
    return pos-offset <= target and pos+offset >= target

def normalizeCam(cam):
    for robot in cam:
        # print(robot)
        robot.x = float(round(1-robot.x,3))
        robot.y = float(round(1-robot.y,3))

def normalizePositions(cam1,cam2):
    # print(cam1,cam2)
    normalizeCam(cam2)
    # print("cam1",cam1)
    # print("cam2",cam2)
    robots = []
    for rob1 in cam1:
        for rob2 in cam2:
            smallerXRob = rob1 if rob1.x < rob2.x else rob2
            largerXRob = rob1 if rob1.x >= rob2.x else rob2
            if nPos(smallerXRob.x,largerXRob.x) and nPos(smallerXRob.y,largerXRob.y,0.1):
                r = rob1.copy()
                r.x = float((abs(smallerXRob.x - largerXRob.x)/2) + smallerXRob.x)
                r.y = float((abs(smallerXRob.y - largerXRob.y)/2) + smallerXRob.y)
                robots.append(r)
    return robots
