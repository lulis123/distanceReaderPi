import RPi.GPIO as GPIO
import time
import requests
import json
def measureDistance(ECHO,TRIG):
    GPIO.output(TRIG, True)
    time.sleep(0.001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == False:
        start = time.time()
    while GPIO.input(ECHO) == True:
        end = time.time()

    return ((end-start)/0.000058)

def postEvent(eventType):
    requestBody = { "eventType": eventType, "storeNumber": 1 }
    requests.post("http://192.168.1.107:5000/event/create",json=requestBody)
    if(eventType == "Entry"):
        print("Registrei uma entrada!")

    else:
        print("Registrei uma saída!")

    time.sleep(0.1)

if __name__ == '__main__':
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    insideTrig = 4
    insideEcho = 18
    outsideTrig = 17
    outsideEcho = 27
    insideVector = []
    outsideVector = []
    measureCounter = 0
    insideMeasure = False
    outsideMeasure = False
    GPIO.setup(insideTrig, GPIO.OUT)
    GPIO.setup(outsideTrig, GPIO.OUT)
    GPIO.setup(insideEcho, GPIO.IN)
    GPIO.setup(outsideEcho, GPIO.IN)



    print("Calculando distância média")
    #Getting the mean value
    for x in range(0,1000):
        time.sleep(0.001)
        insideVector.append(measureDistance(insideEcho,insideTrig))
        outsideVector.append(measureDistance(outsideEcho,outsideTrig))

    averageInside = sum(insideVector)/len(insideVector)
    averageOutside = sum(outsideVector)/len(outsideVector)

    print("Cálculo finalizado!")

    while True:
        time.sleep(0.01)
        if(measureCounter == 0):
            insideMeasure = False
            outsideMeasure = False

        if(measureCounter > 0):
            measureCounter = measureCounter - 1

        distanceInside = measureDistance(insideEcho,insideTrig)
        distanceOutside = measureDistance(outsideEcho,outsideTrig)

        if abs(distanceInside - averageInside) >= 30:
            if outsideMeasure == True:
                postEvent("Entry")
                outsideMeasure = False
                measureCounter = 0
            else:
                insideMeasure = True
                measureCounter = 50
        
        if abs(distanceOutside-averageOutside) >= 30:
            if insideMeasure == True:
                postEvent("Exit")
                insideMeasure = False
                measureCounter = 0
            else:
                outsideMeasure = True
                measureCounter = 50
    GPIO.cleanup()
