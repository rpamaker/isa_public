from datetime import timedelta, datetime


def get_date_range(desde_str, hasta_str):
    desde_dt = datetime.strptime(desde_str, '%d/%m/%Y')
    hasta_dt = datetime.strptime(hasta_str, '%d/%m/%Y')

    date_range = []
    for n in range(int((hasta_dt - desde_dt).days) + 1):
        date3 = desde_dt + timedelta(n)
        date_formatted = date3.strftime('%d/%m/%Y')
        date_range.append(date_formatted)

    return date_range


