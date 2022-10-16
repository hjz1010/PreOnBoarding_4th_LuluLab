import json
import uuid

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q
from django.db         import transaction

from core.utils import *
from reservations.models import *
from users.models        import User

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

class ReservationView(View):
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
                        
            with transaction.atomic():
                # 1. 먼저 예약자 테이블에 예약자 생성 or 가져오기
                booker, is_created = User.objects.get_or_create(
                    name         = booker_name,
                    contact      = booker_phone,
                    is_blacklist = False 
                )
                            
                # 2. 중복 예약 불가
                # 동일 예약 검사 : 예약자 + 환자 이름 + 환자 생년월일 + 병원 + 날짜 + 시간이 똑같나 확인
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
                                    
                # 3. 예약하기
                Reservation.objects.create(
                    reservation_number = str(booker.id)+str(hospital_id.id)+date.replace('-','')+str(time_id.id),
                    customer           = booker,
                    patient_name       = patient_name,
                    patient_birth      = patient_birth,
                    hospital           = hospital_id,
                    reservation_type   = reservation_type_id,
                    reservation_status = ReservationStatus.objects.get(id=1),  # 기본값 설정 안했으니까 1번값(예약완료)으로 넣기
                    date               = date,
                    time               = time_id,
                )
                
                reservation_result = {
                    'reservation_code' : '예약코드',  # 팀원들과 의논하기
                    'booker_name' : booker.name
                }
            
            return JsonResponse({'message': 'SUCCESS', 'reservation_result': reservation_result}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Hospital.DoesNotExist:
            return JsonResponse({'message': 'HOSPITAL_DOES_NOT_EXIST'}, status=404)
        except ReservationType.DoesNotExist:
            return JsonResponse({'message': 'RESERVATION_TYPE_DOES_NOT_EXIST'}, status=404)
        except Time.DoesNotExist:
            return JsonResponse({'message': 'TIME_DOES_NOT_EXIST'}, status=404)

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