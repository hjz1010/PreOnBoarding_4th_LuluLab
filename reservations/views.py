from datetime import datetime, timedelta

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q
from django.utils      import timezone

from reservations.models import *

'''
1. 예약가능한 목록 
Method : get
query string으로 조건을 받아온다.
- 조건: 지역 / 타입  (조건 없으면 전체)
조건에 해당하는 병원만 DB에서 가져온다.
가져온 병원의 리스트를 반환한다.
'''

class HospitalListView(View):
    def get(self, request):
        try: 
            # 검색 조건으로 지역 또는 타입을 id 값으로 받는다
            province_id      = request.GET.get('province', None)
            hospital_type_id = request.GET.get('type', None)

            q = Q()

            if province_id :
                Province.objects.get(id=province_id)
                q &= Q(province_id = province_id)

            if hospital_type_id :
                HospitalType.objects.get(id=hospital_type_id)
                q &= Q(hospital_type_id = hospital_type_id)

            hospitals = Hospital.objects.filter(q)

            hospital_list = [{
                'id' : hospital.id,
                'name' : hospital.name,
                'address' : hospital.address,
                'contact' : hospital.contact,
                'type' : hospital.hospital_type.type,
                'province' : hospital.province.name
            } for hospital in hospitals]

            return JsonResponse({'message': 'SUCCESS', 'result': hospital_list}, status=200)
        except Province.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PROVINCE_ID'}, status=404)
        except HospitalType.DoesNotExist:
            return JsonResponse({'message': 'INVALID_TYPE_ID'}, status=404)

'''
2. 병원의 예약 가능 일시를 확인할 수 있습니다.
Method: get
path parameter로 병원_id를 받아온다.
해당 병원의 예약 가능한 날짜를 반환한다.
- 조회하는 날짜+1 ~ +7일만 예약 가능으로 조회
- 해당 날짜에 속하는 예약 데이터를 가져온 뒤
- 반환하는 예약 가능 일시에서 제외한다.

* today = 현재 날짜 
* 조회 날짜 = today + timedelta(days=1)  ~  today + timedelta(days=7)
* 각 날짜마다 각 타임의 예약이 있는지 필터링 후 없는 값만 리스트에 추가
'''

class DateTimeView(View):
    def get(self, request, hospital_id):
        try:
            today = timezone.now()
            print('############## today: ', today) # 2022-10-15 07:04:51.594988+00:00 
            ##### timezone 문제 해결해야 함

            bookable_datetime = {}
            # 반환하려는 형태
            # { '2022-10-10' : ['9:00', '14:00'],
            #   '2022-10-11' : ['11:00', '15:00', '16:00'],
            #   '2022-10-12' : [],
            #   '2022-10-13' : ['17:00'],
            #    ...
            # } 

            for i in range(1,8):  # 코드가 넘 못생겼다 리펙토링해봐야겠다
                date = today + timedelta(days=i)
                
                time_list          = [time.time for time in Time.objects.all()]
                booked_time_list   = [reservation.time.time 
                                      for reservation in Reservation.objects.filter(hospital_id=hospital_id ,date=date)]
                bookable_time_list = sorted(list(set(time_list)-set(booked_time_list)))
                
                date = date.strftime("%Y-%m-%d")
                bookable_datetime[date] = bookable_time_list

            return JsonResponse({'message': 'SUCCESS', 'result': bookable_datetime}, status=200)
        except Province.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PROVINCE_ID'}, status=404)
        except HospitalType.DoesNotExist:
            return JsonResponse({'message': 'INVALID_TYPE_ID'}, status=404)
