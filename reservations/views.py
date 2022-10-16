import json
import datetime
import base64
import hashlib
import hmac
import requests
import time as time_

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import Q
from django.db           import transaction

from core.utils          import *
from reservations.models import *
from users.models        import User

from Lululab.settings    import (
    SMS_SERVICE_ID,
    FROM_NUMBER,
    ACCESS_KEY_ID,
    NAVER_SECRET_KEY
    )


# 예약 가능한 병원 목록
class HospitalListView(View):
    def get(self, request):
        try: 
            # 검색 조건으로 지역 또는 타입을 id 값으로 받는다
            province_id      = request.GET.get('province', None)
            hospital_type_id = request.GET.get('type', None)

            q = Q(is_available = True)

            if province_id :
                Province.objects.get(id=province_id)
                q &= Q(province_id = province_id)

            if hospital_type_id :
                HospitalType.objects.get(id=hospital_type_id)
                q &= Q(hospital_type_id = hospital_type_id)

            hospitals = Hospital.objects.filter(q)

            hospital_list = [{
                'id'       : hospital.id,
                'name'     : hospital.name,
                'address'  : hospital.address,
                'contact'  : hospital.contact,
                'type'     : hospital.hospital_type.type,
                'province' : hospital.province.name
            } for hospital in hospitals]

            return JsonResponse({'message': 'SUCCESS', 'result': hospital_list}, status=200)
        except Province.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PROVINCE_ID'}, status=404)
        except HospitalType.DoesNotExist:
            return JsonResponse({'message': 'INVALID_TYPE_ID'}, status=404)

# 특정 병원의 예약 가능한 일시
class DateTimeView(View):
    def get(self, request, hospital_id):
        try:
            Hospital.objects.get(id=hospital_id) # 병원 id값이 유효한지 확인

            result = {}
            # 예약가능 일시 
            # { '2022-10-10' : ['9:00', '14:00'],
            #   '2022-10-11' : ['11:00', '15:00', '16:00'],
            #   '2022-10-12' : [],
            #   '2022-10-13' : ['17:00'],
            #    ...
            # } 

            for date_to_add in range(ADD_TO_START_DATE, ADD_TO_END_DATE+1):  
                available_date     = DATE_TODAY + datetime.timedelta(days=date_to_add)
                
                opening_time_list  = list(Time.objects.values_list('time', flat=True))
                reserved_time_list = [reservation.time.time \
                                        for reservation in Reservation.objects \
                                            .filter(hospital_id=hospital_id, \
                                                    date=available_date, \
                                                    reservation_status_id=ReservationStatusEnum.RESERVED.value)] 
                available_time_list = sorted(list( \
                                        set(opening_time_list)-set(reserved_time_list) ))
                
                available_date         = available_date.strftime("%Y-%m-%d")
                result[available_date] = available_time_list

            return JsonResponse({'message': 'SUCCESS', 'result': result}, status=200)
        except Hospital.DoesNotExist:
            return JsonResponse({'message': 'INVALID_HOSPITAL_ID'}, status=404)

class ReservationView(View):
    def	make_signature(self):
        timestamp = str(int(time_.time() * 1000))
        access_key = ACCESS_KEY_ID				# access key id (from portal or Sub Account)
        secret_key = NAVER_SECRET_KEY				# secret key (from portal or Sub Account)
        secret_key = bytes(secret_key, 'UTF-8')

        method = "POST"
        uri = "/sms/v2/services/" + SMS_SERVICE_ID + "/messages"

        message = method + " " + uri + "\n" + timestamp + "\n"+ access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def post(self, request):
        data = json.loads(request.body)
        try:
            booker_name         = data['booker_name']
            booker_phone        = data['booker_phone']
            patient_name        = data['patient_name']
            patient_birth       = data['patient_birth']
            hospital_id         = Hospital.objects.get(id=data['hospital_id'])
            reservation_type_id = ReservationType.objects.get(id=data['reservation_type_id']) 
            date                = data['date']
            time_id             = Time.objects.get(id=data['time_id'])
                        
            # 이름, 연락처, 생년월일, 날짜 유효성 체크
            check_vaild_name_format(booker_name)
            check_valid_contact_format(booker_phone)
            check_vaild_name_format(patient_name)
            check_valid_date_format(patient_birth)
            check_valid_date_format(date)
            
            # 당일 예약 불가
            if date <= str(DATE_TODAY):
                return JsonResponse({'message': f'CHOOSE_ANY_DAY_AFTER_{str(DATE_TODAY)}'}, status=400)
            
            # 연락처 중복 불가
            already_exist_contact = User.objects.filter(contact=booker_phone)
            
            if already_exist_contact.exists():
                user_name = [user.name for user in already_exist_contact]
                if user_name[0] != booker_name:
                    return JsonResponse({'message': 'SAME_CONTACT_ALREADY_EXIST'}, status=409)

            with transaction.atomic():
                # 1. 먼저 예약자 테이블에 예약자 생성 or 가져오기
                booker, is_created = User.objects.get_or_create(
                    name         = booker_name,
                    contact      = booker_phone
                )
                                        
                # 2. 중복 예약 불가 : 예약자 + 환자 이름 + 환자 생년월일 + 병원 + 날짜 + 시간 일치 여부 확인
                already_exist_revervation = Reservation.objects.filter(
                                                customer      = booker,
                                                patient_name  = patient_name,
                                                patient_birth = patient_birth,
                                                hospital      = hospital_id,
                                                date          = date,
                                                time_id       = time_id
                                            ).exists()
                    
                if already_exist_revervation:
                    return JsonResponse({'message': 'SAME_RESERVATION_ALREADY_EXIST'}, status=409)
                            
                reservation_code = str(booker.id)+str(hospital_id.id)+date.replace('-','')+str(time_id.id)
                
                
                # 3. 예약하기
                Reservation.objects.create(
                    reservation_number = reservation_code,
                    customer           = booker,
                    patient_name       = patient_name,
                    patient_birth      = patient_birth,
                    hospital           = hospital_id,
                    reservation_type   = reservation_type_id,
                    reservation_status = ReservationStatus.objects.get(id=ReservationStatusEnum.RESERVED.value),
                    date               = date,
                    time               = time_id,
                )
            
                reservation_result = {
                    'reservation_code': reservation_code,
                    'booker_name'     : booker.name
                }

            url            = "https://sens.apigw.ntruss.com/sms/v2/services/"+SMS_SERVICE_ID+"/messages"
            timestamp      = str(int(time_.time() * 1000))
            access_key     = ACCESS_KEY_ID
            signature      = self.make_signature()

            headers        = { 
                "Content-Type"            : "application/json",
                "x-ncp-apigw-timestamp"	  : timestamp,
                'x-ncp-iam-access-key'    : access_key,
                'x-ncp-apigw-signature-v2': signature
            }

            body           = {
                "type"    : "SMS",
                "from"    : FROM_NUMBER,
                "countryCode":"82",
                "messages":[{"to":booker_phone.replace('-',''),}],
                "content" : "{}님 {}일 {}시 {} {}예약.\n예약번호는 [{}]입니다.".format(booker_name, date, time_id.time.strftime("%H:%M"), hospital_id.name, reservation_type_id.type, reservation_code)
            }

            body          = json.dumps(body)
            response      = requests.post(url, headers=headers, data=body)
            response_dict = response.json()
            print(response_dict)
            status_code   = response_dict['statusCode'] if 'statusCode' in response_dict else response_dict['errorMessage']

            if int(status_code) != 202:
                return JsonResponse({"message": "SMS_SEND_FAIL"}, status=400)
            
            return JsonResponse({'message': 'SUCCESS', 'reservation_result': reservation_result}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Hospital.DoesNotExist:
            return JsonResponse({'message': 'HOSPITAL_DOES_NOT_EXIST'}, status=404)
        except ReservationType.DoesNotExist:
            return JsonResponse({'message': 'RESERVATION_TYPE_DOES_NOT_EXIST'}, status=404)
        except Time.DoesNotExist:
            return JsonResponse({'message': 'TIME_DOES_NOT_EXIST'}, status=404)
        except ValueError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status = 400)

    def patch(self, request, reservation_number):
        '''
        신청한 예약 번호를 통해 예약을 변경할 수 있습니다. (환자 이름, 예약 시간, 예약 종류 변경 가능)
        '''
        try:
            data = json.loads(request.body)

            new_patient_name        = data['patient_name']
            new_patient_birth       = data['patient_birth']
            new_date                = data['date']
            new_time_id             = data['time_id'] # 1-8까지값
            new_reservation_type_id = data['reservation_type_id'] # 1. 진료 2. 검진

            #환자변경: 이름 & 생년원일, 예약날짜변경: 날짜 & 시간 둘다 있어야함
            check_both_or_none(new_patient_name, new_patient_birth, "NAME", "BIRTHDAY")
            check_both_or_none(new_date, new_time_id, "DATE", "TIME")

            if new_patient_name and new_patient_birth: 
                check_vaild_name_format(new_patient_name)
                check_valid_date_format(new_patient_birth)

            if new_date and new_time_id: 
                check_valid_date_format(new_date)
                check_valid_time_id(new_time_id)
                #변경하려는 날짜는 내일 이후여야 함
                if new_date <= str(DATE_TODAY):
                    return JsonResponse({'message': f'CHOOSE_ANY_DAY_AFTER_{str(DATE_TODAY)}'}, status=400)

            if new_reservation_type_id: check_valid_reservation_type_id(new_reservation_type_id)

            #변경하려는 예약
            reservation = Reservation.objects.get(reservation_number=reservation_number)
            
            #원래 예약 날짜가 오늘 이전이면 변경불가
            if reservation.date <= DATE_TODAY:
                return JsonResponse({'message': 'RESERVATION_CANNOT_BE_CHANGED'}, status=400)
            
            if new_patient_name and new_patient_birth: 
                reservation.patient_name  = new_patient_name
                reservation.patient_birth = new_patient_birth

            if new_date and new_time_id:
                #시간변경시 변경하려는 예약시간에 다른 예약이 있으면 변경 불가
                is_already_exist = Reservation.objects.filter(
                    hospital_id = reservation.hospital_id,
                    date        = new_date,
                    time_id     = new_time_id
                )
                if is_already_exist:
                    return JsonResponse({'message': 'CHOOSE_ANOTHER_DATE_OR_TIME'}, status=400)
                reservation.date    = new_date
                reservation.time_id = new_time_id

            if new_reservation_type_id:
                reservation.reservation_type_id = new_reservation_type_id

            reservation.save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except Reservation.DoesNotExist:
            return JsonResponse({'message': 'RESERVATION_DOES_NOT_EXIST'}, status = 404)
        except ValueError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status = 400)



class ResevationListView(View):
	def get(self, request):
		data = json.loads(request.body)
        # 입력값이 사용자 이름인지 확인.
		booker_name = User.objects.filter(name = data.get('name_or_number'))

		if booker_name.exists():
			reservations = Reservation.objects.filter(customer__in = booker_name).order_by('date')
		# 아니라면 예약 번호인지 확인, 둘다 아니라면 예외 처리
		else:
			reservation_number_info = Reservation.objects.filter(reservation_number = data.get('name_or_number'))
			if reservation_number_info.exists():				
				reservations = reservation_number_info
	
			elif not booker_name.exists() and not reservation_number_info.exists():
				return JsonResponse({'MESSAGE' : 'RESERVATION_DOES_NOT_EXIST'}, status=404)

		result = [{
			'reservation_number' : reservation.reservation_number,
			'patient_name' : reservation.patient_name,
			'patient_birth' : reservation.patient_birth,
			'date' : reservation.date,
			'customer' : reservation.customer.name,
			'time' : reservation.time.time,
			'hospital  ' : reservation.hospital.name,
			'reservation_type' : reservation.reservation_type.type,
			'reservation_status' : reservation.reservation_status.status
		}for reservation in reservations]

		return JsonResponse({'result' : result }, status = 200)
        