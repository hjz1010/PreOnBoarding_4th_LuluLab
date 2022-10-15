import json

from django.http  import JsonResponse
from django.views import View

from core.utils import *
from reservations.models import Reservation

class ReservationView(View):

    def patch(self, request, reservation_number):
        '''
        신청한 예약 번호를 통해 예약을 변경할 수 있습니다. (환자 이름, 예약 시간, 예약 종류 변경 가능)

        요청 PATCH /reservations/<reservation_number> 특정예약에대한수정이니까 path parameter
        
        req.body
        {
            patient_name: 변경할이름.null이면 변경 안함,
            patient_birth: 변경할 생일. 이름이랑 생일은 같이 들어와야함
            date: 변경할 날짜. null이면 변경 안함,
            time_id: 변경할 시간. null이면 변경 안함,
            reservation_type_id: 변경할 예약 종류, null이면 변경 안함.
        }
        '''
        try:
            data = json.loads(request.body)

            new_patient_name = data['patient_name']
            new_patient_birth = data['patient_birth'] 
            # name과 birth는 동시에 들어와야함 하나만 있으면: xor true면 에러 bool(a) ^ bool(b)
            new_date = data['date']
            new_time_id = data['time_id'] # 1-8까지값
            # date랑 time도 바꿀거면 둘다주기
            new_reservation_type_id = data['reservation_type_id'] # 1. 진료 2. 검진

            #환자변경은 이름 & 생년원일 둘다 있어야함
            check_both_or_none(new_patient_name, new_patient_birth, "NAME", "BIRTHDAY")
            #날짜변경도 날짜 & 시간 둘다
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
                reservation.date = new_date
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