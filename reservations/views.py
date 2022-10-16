from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q

from reservations.models import *

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