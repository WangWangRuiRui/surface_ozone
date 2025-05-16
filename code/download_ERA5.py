# -*- coding: utf-8 -*-
import cdsapi
import winsound

c = cdsapi.Client()
lines = open("2021.txt", 'r').readlines()

duration = 5000
freq = 440

for i in range(len(lines)):
    if i >= 0:
        lines[i] = lines[i].replace('\n', '')
        print(lines[i])
        fields = lines[i].split('/')  # split data
        name = fields[0]
        # fields = lines[i].split(' ') #split data
        # print(fields)
        # year = fields[0]
        # month = fields[1]
        # day = fields[2]
        # print(' Download %s-%s-%s data ' %(year,month,day))#,end=""

        c.retrieve(
            'cams-global-reanalysis-eac4',
            {
                'format': 'netcdf',
                'time': [
                    '00:00', '03:00', '06:00',
                    '09:00', '12:00', '15:00',
                    '18:00', '21:00',
                ],
                'variable': 'ozone',
                # 'pressure_level': '1000',
                'date': lines[i],  # '2013-01-01/2013-12-31',
                'model_level': '60',
            },
            # 'reanalysis' + ' %s%s%s' % (year,month,day)+ '.nc')
            # print('reanalysis%s%s%s' % (year,month,day)+'.nc download successful')
            'cams_reanalysis' + name + '.nc')
        print('cams_reanalysis' + name + '.nc download successful')
    else:
        pass

winsound.Beep(freq, duration)