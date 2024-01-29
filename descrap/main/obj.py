import cv2
from datetime import datetime
from django.templatetags.static import static

def objd(path):
    date = datetime.now()
    name = date.strftime('%H:%M')

    img = cv2.imread(path)
    classNames = []
    identified = []
    pricing = {
    
    "BICYCLE": "15",
    "CAR": "50",
    "MOTORCYCLE": "30",
    "AIRPLANE": "100",
    "BUS": "40",
    "TRAIN": "30",
    "TRUCK": "50",
    "BOAT": "60",
    "TRAFFIC LIGHT": "5",
    "FIRE HYDRANT": "8",
    "STREET SIGN": "7",
    "STOP SIGN": "10",
    "PARKING METER": "5",
    "BENCH": "5",
    "BIRD": "2",
    "CAT": "8",
    "DOG": "8",
    "HORSE": "15",
    "SHEEP": "12",
    "COW": "20",
    "ELEPHANT": "50",
    "BEAR": "40",
    "ZEBRA": "20",
    "GIRAFFE": "30",
    "HAT": "5",
    "BACKPACK": "10",
    "UMBRELLA": "7",
    "SHOE": "5",
    "EYE GLASSES": "8",
    "HANDBAG": "12",
    "TIE": "8",
    "SUITCASE": "15",
    "FRISBEE": "10",
    "SKIS": "20",
    "SNOWBOARD": "25",
    "SPORTS BALL": "15",
    "KITE": "10",
    "BASEBALL BAT": "10",
    "BASEBALL GLOVE": "8",
    "SKATEBOARD": "15",
    "SURFBOARD": "20",
    "TENNIS RACKET": "12",
    "BOTTLE": "5",
    "PLATE": "4",
    "WINE GLASS": "6",
    "CUP": "4",
    "FORK": "3",
    "KNIFE": "3",
    "SPOON": "3",
    "BOWL": "4",
    "BANANA": "2",
    "APPLE": "2",
    "SANDWICH": "5",
    "ORANGE": "2",
    "BROCCOLI": "4",
    "CARROT": "3",
    "HOT DOG": "5",
    "PIZZA": "7",
    "DONUT": "3",
    "CAKE": "10",
    "CHAIR": "10",
    "COUCH": "15",
    "POTTED PLANT": "8",
    "BED": "20",
    "MIRROR": "8",
    "DINING TABLE": "15",
    "WINDOW": "5",
    "DESK": "10",
    "TOILET": "15",
    "DOOR": "10",
    "TV": "30",
    "LAPTOP": "25",
    "MOUSE": "5",
    "REMOTE": "8",
    "KEYBOARD": "8",
    "CELL PHONE": "15",
    "MICROWAVE": "20",
    "OVEN": "25",
    "TOASTER": "8",
    "SINK": "10",
    "REFRIGERATOR": "30",
    "BLENDER": "15",
    "BOOK": "5",
    "CLOCK": "5",
    "VASE": "8",
    "SCISSORS": "5",
    "TEDDY BEAR": "10",
    "HAIR DRIER": "10",
    "TOOTHBRUSH": "5",
    "HAIR BRUSH": "5",
    # Add more objects and prices as needed
}

    classFile = './datasets/coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = './datasets/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = './datasets/frozen_inference_graph.pb'
    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
  
    if classIds is not None:
        
        
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            identified.append(classNames[classId - 1].upper())

        cv2.imwrite(f"ack.png", img)

        # Loop through the items in identified and calculate the total price and show the price of each item in front of it
        total = 0
        finalprice = []
        no_item = len(identified)
        for item in identified:
            if item in pricing:
                finalprice.append(pricing[item])
                total += int(pricing[item])
            else:
                identified.remove(item)
                identified.append(f"{item} (Not Currently Accepted)")

        return identified, finalprice, total, no_item
    else:
        # No objects detected
        return ["No valid objects detected"], [0], 0, 0
