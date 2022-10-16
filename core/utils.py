import re
import datetime
from enum import Enum

DATE_TODAY = datetime.date.today()

class ReservationTypeEnum(Enum): 
    TREATMENT = 1 # 진료..치료?
    CHECKUP   = 2 # 검진

class ReservationStatusEnum(Enum): 
    RESERVED = 1 # 예약완료
    VISITED  = 2 # 방문완료
    NOSHOW   = 3 # 노쇼
    
def check_vaild_name_format(value):
    REGEX_NAME = '^[가-힣]{2,5}$'
    if not re.match(REGEX_NAME, value):
        raise ValueError("INVALID_NAME")

def check_valid_date_format(value):
    REGEX_DATE = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
    if not re.match(REGEX_DATE, value):
        raise ValueError("INVALID_DATE_FORMAT")

def check_valid_time_id(value):
    if not value in range(1,9):
        raise ValueError("INVALID_TIME_ID")

def check_valid_reservation_type_id(value):
    types = [type.value for type in ReservationTypeEnum]
    if not value in types:
        raise ValueError("INVALID_RESERVATION_TYPE_ID")

def check_both_or_none(val1, val2, str1, str2):
    if bool(val1) ^ bool(val2):
        raise ValueError(f"BOTH_{str1}_AND_{str2}_REQUIRED_OR_NONE_SHOULD_BE_GIVEN")
