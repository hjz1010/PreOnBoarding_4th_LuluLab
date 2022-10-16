import json
import uuid

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q
from django.db         import transaction


from reservations.models import *
from users.models        import User

# 예약 가능한 병원 목록
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
