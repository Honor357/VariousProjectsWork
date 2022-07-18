from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR


## example input
#month="05/2022"
## example output
#date="27.05.2022"

def get_last_friday(month):
    friday = datetime.strptime(month, '%m/%Y') + relativedelta(weekday=FR(-1), day=31)
    #offset = (date_time.weekday() - 4) % 7
    #friday = date_time - timedelta(days=offset)
    return friday.strftime("%d.%m.%Y")

## selftest
#date==get_last_friday(month)
