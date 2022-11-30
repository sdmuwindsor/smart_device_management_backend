from app.mqtt.mqtt_connection import mqtt_connection

class mqtt_control:
    
    mqttDeviceObjList = []

    @staticmethod
    def add_a_device(device_id, device_type, binaryControl=False):
        if device_type=="light":
            if binaryControl:
                states = ["0","1"]
            else:
                states = list(str(i) for i in range(101))
            tmp = mqtt_connection(device_id,device_type,states)
            j = {"device_id":device_id,"device_type":device_type,"sensor_states":[states],"mqttConnection":[tmp]}
        elif device_type=="thermostat":
            temp_states = list(str(i) for i in range(50,101,1))
            tmp = mqtt_connection(device_id,"temperature",states)
            humidity_states = list(str(i) for i in range(10,81,1))
            tmp1 = mqtt_connection(device_id,"humidity",states)
            j = {"device_id":device_id,"device_type":device_type,"sensor_states":[temp_states,humidity_states],"mqttConnection":[tmp,tmp1]}
        for i in j['mqttConnection']:
            i.connect_sensor()
        mqtt_control.mqttDeviceObjList.append(j)
        return True

    @staticmethod
    def turn_off_device(device_id, device_type):
        if device_type=="light":
            for i in mqtt_control.mqttDeviceObjList:
                if i['device_id'] == device_id:
                    i['mqttConnection'][0].update_sensor_state('0')
                    return True
        return False

    @staticmethod
    def disconnect_device(device_id):
        for i in mqtt_control.mqttDeviceObjList:
            if i['device_id'] == device_id:
                for j in i['mqttConnection']:
                    mqtt_connection.disconnect_sensor(device_id)
                return True
        return False

    @staticmethod
    def is_connected(device_id):
        for i in mqtt_control.mqttDeviceObjList:
            if i['device_id'] == device_id:
                tmp=True
                for j in i['mqttConnection']:
                    tmp = tmp and j.check_sensor_connection_status()
                return tmp
        return False

    @staticmethod
    def get_device_values(device_id):
        for i in mqtt_control.mqttDeviceObjList:
            if i['device_id'] == device_id:
                tmp = []
                for j in i['mqttConnection']:
                    tmp.append(j.get_state())
                return tmp
        return []
