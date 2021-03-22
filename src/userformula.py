import numpy as np
import pandas as pd
import src.settings as settings
import src.programTools as programTools

def user_equations(data):
    '''
    Take data and process users equations in the entire database, reducing size poping inused columns.
    :param data: pandas dataframe containing data
    :return: pandas dataframe with updated data
    '''

    data.loc[(data['RPM'] > 2000) & (data['EngineTemp'] > 84), 'HalfFan'] = 1
    data.loc[(data['RPM'] < 2000) | (data['EngineTemp'] < 84), 'HalfFan'] = 0
    data.loc[(data['RPM'] > 2000) & (data['EngineTemp'] > 94), 'FullFan'] = 1
    data.loc[(data['RPM'] < 2000) | (data['EngineTemp'] < 94), 'FullFan'] = 0

    data['A_9_map'] = programTools.bandPassFilter(data['A_9_map'])
    '''
    sensor_data_a = data['GPSlatHW']
    sensor_data_b = data['GPSlatLW']
    sensor_data_c = data['GPSlongHW']
    sensor_data_d = data['GPSlongLW']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)

    gpsLat = ((data['GPSlatHW']-65536) * 65536 + data['GPSlatLW'])/10000000
    gpsLong = ((data['GPSlongHW']-65536) * 65536 + data['GPSlongLW'])/10000000
    '''

    data['GPSLat'] = ((data['GPSlatHW']-65536) * 65536 + data['GPSlatLW'])/10000000
    data['GPSLong'] = ((data['GPSlongHW']-65536) * 65536 + data['GPSlongLW'])/10000000

    '''
    sensor_data_a = data['GForceLat']
    sensor_data_b = -data['GForceLong']
    sensor_data_c = -data['gyro_z']
    sensor_data_e = data['Speed']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_f = pd.to_numeric(sensor_data_f)
    '''

    sensor_data = pd.to_numeric(data['SteeringAngle'])
    sensor_data.loc[sensor_data > 3276.8] = sensor_data.loc[sensor_data > 3276.8] - 6553.6
    data['SteeringAngle'] = sensor_data

    sensor_data = pd.to_numeric(data['ECU_GForceLat'])
    sensor_data.loc[sensor_data > 32.768] = sensor_data.loc[sensor_data > 32.768] - 65.536
    data['ECU_GForceLat'] = sensor_data

    cutFs = 5
    data['GForceLat'] = programTools.bandPassFilter(data['GForceLat'], cutf=cutFs, order=5)
    data['GForceLong'] = programTools.bandPassFilter(-data['GForceLong'], cutf=cutFs, order=5)
    cutFs = 1
    data['gyro_z'] = programTools.bandPassFilter(-data['gyro_z'], cutf=cutFs, order=5)

    '''
    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']
    sensor_data_e = data['Speed']
    sensor_data_x = -data['GForceLong']
    sensor_data_y = data['GForceLat']
    sensor_data_z = data['GForceVert']
    sensor_data_tps = data['TPS']
    sensor_data_bp = data['BrakePressure']
    sensor_data_sa = data['SteeringAngle']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_sa = pd.to_numeric(sensor_data_sa)
    '''

    cutFs = 12

    data['LVDTFL'] = programTools.bandPassFilter(data['LVDTFL'], cutf=cutFs, order=5)
    data['LVDTFR'] = programTools.bandPassFilter(data['LVDTFR'], cutf=cutFs, order=5)
    data['LVDTRL'] = programTools.bandPassFilter(data['LVDTRL'], cutf=cutFs, order=5)
    data['LVDTRR'] = programTools.bandPassFilter(data['LVDTRR'], cutf=cutFs, order=5)
    '''    filteredsignal_x = ncuTools.bandPassFilter(sensor_data_x, cutf=5, order=5)
    filteredsignal_y = ncuTools.bandPassFilter(sensor_data_y, cutf=5, order=5)
    filteredsignal_z = ncuTools.bandPassFilter(sensor_data_z, cutf=5, order=5)'''

    data['LVDTFL'] = programTools.mapDouble(data['LVDTFL'], 0.59, 0.65, 206, 196)
    data['LVDTFR'] = programTools.mapDouble(data['LVDTFR'], 0.9, 0.94, 206, 196)
    data['LVDTRL'] = programTools.mapDouble(data['LVDTRL'], 0.92, 1.02, 221, 216)
    data['LVDTRR'] = programTools.mapDouble(data['LVDTRR'], 0.76, 0.8, 221, 216)

    '''    
    filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)'''

    diff1 = np.diff(data['LVDTFL']) / np.diff(data['time'])
    diff2 = np.diff(data['LVDTFR']) / np.diff(data['time'])
    diff3 = np.diff(data['LVDTRL']) / np.diff(data['time'])
    diff4 = np.diff(data['LVDTRR']) / np.diff(data['time'])

    diff1 = np.append(diff1, 0)
    diff2 = np.append(diff2, 0)
    diff3 = np.append(diff3, 0)
    diff4 = np.append(diff4, 0)

    data['diffLVDTFL'] = diff1
    data['diffLVDTFR'] = diff2
    data['diffLVDTRL'] = diff3
    data['diffLVDTRR'] = diff4

    #diffdata_a = ncuTools.bandPassFilter(diffdata_a, cutf=cutFs, order=5)
    #diffdata_b = ncuTools.bandPassFilter(diffdata_b, cutf=cutFs, order=5)
    #diffdata_c = ncuTools.bandPassFilter(diffdata_c, cutf=cutFs, order=5)
    #diffdata_d = ncuTools.bandPassFilter(diffdata_d, cutf=cutFs, order=5)

    altFront = data['LVDTFL'] / 2 + data['LVDTFR'] / 2
    altRear = data['LVDTRL'] / 2 + data['LVDTRR'] / 2
    cutFsAlt = 5
    data['altFront'] = programTools.bandPassFilter(altFront, cutf=cutFsAlt, order=2)
    data['altRear'] = programTools.bandPassFilter(altRear , cutf=cutFsAlt, order=2)

    data = data.drop(columns = ['GPSlatHW','GPSlongHW','GPSlatLW','GPSlongLW','max_enable','CAN_ID','CAN_byte[0]' ,'CAN_byte[1]' ,'CAN_byte[2]','CAN_byte[3]','CAN_byte[4]','CAN_byte[5]','CAN_byte[6]', 'CAN_byte[7]', 'A_1','A_4','A_5','A_6','A_9', 'A_1_map','A_4_map','A_5_map','A_6_map', 'LVDTFLmap','LVDTFRmap','LVDTRRmap','LVDTRLmap', 'O_1', 'O_2', 'O_3'])
    data = data.dropna(axis = 1, how = 'all')

    return data


