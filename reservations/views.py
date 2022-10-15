import json
from unicodedata import name
import uuid

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from reservations.models import Hospital, Reservation, ReservationStatus, ReservationType, Time
from users.models        import User

class ResevationListView(View):
	def get(self, request):
		data = json.loads(request.body)

		booker = User.objects.filter(name = data.get('name_or_number'))

		if booker.exists():
			reservations = Reservation.objects.filter(customer__contains = booker).order_by('date')
		
		else:
			reservation_number_info = Reservation.objects.filter(reservation_number__contains = data.get('name_or_number'))
			if reservation_number_info.exists():				
				reservations = reservation_number_info
	
			elif not booker.exists() and not reservation_number_info.exists():
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

class ReservationView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            booker_name         = data['booker_name']
            booker_phone        = data['booker_phone']
            patient_name        = data['patient_name']
            patient_birth       = data['patient_birth']
            hospital_id         = Hospital.objects.get(id=data['hospital_id'])
            reservation_type_id = ReservationType.objects.get(id=data['reservation_type_id'])  # 1:진료, 2:검진
            date                = data['date']
            time_id             = Time.objects.get(id=data['time_id'])  # 1번-9:00, 2번-10:00, 3번-11:00, 4번-13:00, 5번-14:00, 6번-15:00, 7번-16:00, 8번-17:00
                        
            with transaction.atomic():
                # 1. 먼저 예약자 테이블에 예약자 생성 or 가져오기
                booker, is_created = User.objects.get_or_create(
                    name         = booker_name,
                    contact      = booker_phone,
                    is_blacklist = False    # 팀원들과 이야기해보기
                )
                
                # 2. 그럼 booker에는 예약자 객체가 담겨있음.
                
                # 3. 중복 예약 불가
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
                    
                # 4. 예약하기
                Reservation.objects.create(
                    reservation_number = booker.id+hospital_id+date.replace('-',''),
                    customer           = booker,
                    patient_name       = patient_name,
                    patient_birth      = patient_birth,
                    hospital           = hospital_id,
                    reservation_type   = reservation_type_id,
                    reservation_status = ReservationStatus.objects.get(id=1),  # 기본값 설정 안했으니까 1번값(예약완료)으로 넣기
                    date               = date,
                    time               = time_id,
                )
            
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Hospital.DoesNotExist:
            return JsonResponse({'message': 'HOSPITAL_DOES_NOT_EXIST'}, status=404)
        except ReservationType.DoesNotExist:
            return JsonResponse({'message': 'RESERVATION_TYPE_DOES_NOT_EXIST'}, status=404)
        except Time.DoesNotExist:
            return JsonResponse({'message': 'TIME_DOES_NOT_EXIST'}, status=404)