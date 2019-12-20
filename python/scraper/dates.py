from datetime import date, timedelta


def dates_in_range(sdate, edate):

    res = []

    sdate = date(sdate[0], sdate[1], sdate[2])   # start date
    edate = date(edate[0], edate[1], edate[2])   # end date

    delta = edate - sdate       # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        res.append(str(day))

    return res
