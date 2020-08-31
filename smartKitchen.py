import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
import os



def main():
    
    #IBM Watson Device Credentials
    organization = "rhdp4i"
    deviceType = "raspberrypi"
    deviceId = "001"
    authMethod = "token"
    authToken = "raspberrypi@001"


    def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        print(cmd.data)

        if cmd.data['reset']:
            main()
                  

    try:
            deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
            deviceCli = ibmiotf.device.Client(deviceOptions)
            #..............................................
                
    except Exception as e:
            print("Caught exception connecting device: %s" % str(e))
            sys.exit()

    deviceCli.connect()

    ###########################################################################
    #Initial Values
    jarPer=50
    jarEn = 1
    jarTh=25
                    
    gasWeight=40
    gasEn=1
    gasTh=10

    count=0
    gasLeak=0
    gasLEN=1
    while True:

        #Values from Jar Sensor
        if jarEn == 1:
            jarPer=jarPer-1
            if jarPer <= jarTh:
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=rN1ocfEdP8wxQUZ7DbzR0gKn6iC9qJeVLOsBI34t2MpjTSmFXWVbBoatpqePwrCKGS7hnZWRI0skL5Ny&sender_id=FSTSMS&message= The jar is about to empty. Less than 25% remaining Refill!!!!&language=english&route=p&numbers=9110837705')
                print(r.status_code)
                print("SMS Sent: Jar is about to Empty")
                jarEn=0
        else:
            if jarPer>0:
                jarPer=jarPer-1
                if jarPer==0:
                    r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=rN1ocfEdP8wxQUZ7DbzR0gKn6iC9qJeVLOsBI34t2MpjTSmFXWVbBoatpqePwrCKGS7hnZWRI0skL5Ny&sender_id=FSTSMS&message=The jar is empty. Refill!!!!&language=english&route=p&numbers=9110837705')
                    print(r.status_code)
                    print("SMS Sent: Jar is Empty")
                    
        

        #Values from Gas Weight Sensor
        if gasEn == 1:
            gasWeight=gasWeight-1
            if gasWeight <= gasTh:
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=rN1ocfEdP8wxQUZ7DbzR0gKn6iC9qJeVLOsBI34t2MpjTSmFXWVbBoatpqePwrCKGS7hnZWRI0skL5Ny&sender_id=FSTSMS&message=The gas cylinder is about to empty&language=english&route=p&numbers=9110837705')
                print(r.status_code)
                print("SMS Sent: Gas is about to Empty")
                gasEn=0

        else:
            if gasWeight>0:
                gasWeight=gasWeight-1
                if gasWeight==0:
                    r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=rN1ocfEdP8wxQUZ7DbzR0gKn6iC9qJeVLOsBI34t2MpjTSmFXWVbBoatpqePwrCKGS7hnZWRI0skL5Ny&sender_id=FSTSMS&message=The gas cylinder is empty. Refill!!!!&language=english&route=p&numbers=9110837705')
                    print(r.status_code)
                    print("SMS Sent: Gas cylinder is Empty")
        

        if gasLEN==1:  
            if count>=30:
                gasLeak=1
                gasLEN=0
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=rN1ocfEdP8wxQUZ7DbzR0gKn6iC9qJeVLOsBI34t2MpjTSmFXWVbBoatpqePwrCKGS7hnZWRI0skL5Ny&sender_id=FSTSMS&message=Emergency!! Gas Leakage&language=english&route=p&numbers=9110837705')
                print(r.status_code)
                print("SMS Sent: Emergency!! Gas Leakage ")
                
            count=count+1          

        if gasLeak==1:
            print("Exhaust fan ON!!")
        else:
            print("Exhaust fan OFF!!")
        
            
                
        data = { 'jarPer': jarPer, 'gasWeight':gasWeight, 'gasLeak':gasLeak }
        print (data)
        def myOnPublishCallback():
            print ("Published jarPercentage = %s %%" % jarPer, "to IBM Watson")

        success = deviceCli.publishEvent("SK", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
                
        deviceCli.commandCallback = myCommandCallback
                
    # Disconnect the device and application from the cloud
    deviceCli.disconnect()

main()

