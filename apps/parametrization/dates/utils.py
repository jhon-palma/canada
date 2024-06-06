from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import json, math



#--------  Function Next date in determinated time

def get_date_dict(date):
    date_list = date.split('-')
    birthday = {}
    if date_list != ['']:
        birthday = {
            'day': int(date_list[2]),
            'month': int(date_list[1]),
            'year': int(date_list[0]) 
        }
    return birthday


#--------  Function Next date in determinated time

def divide(number_one, number_two, decimal_place=2):
    quotient = number_one/number_two
    remainder = number_one % number_two
    if remainder != 0:
        quotient_str = str(quotient)
        for loop in range(0, decimal_place):
            if loop == 0:
                quotient_str += "."
            surplus_quotient = (remainder * 10) / number_two
            quotient_str += str(surplus_quotient)
            remainder = (remainder * 10) % number_two
            if remainder == 0:
                break
        return float(quotient_str)
    else:
        return quotient


#--------  Function Next date in determinated time

def next_date(date, var, ammount):
    if var == 'days':
        new_date = date + relativedelta(days=+ammount)
    if var == 'months':
        new_date = date + relativedelta(months=+ammount)
    return new_date


#--------  Function Previous date in determinated time

def previous_date(date, var, ammount):
    if var == 'days':
        new_date = date - relativedelta(days=ammount)
    if var == 'months':
        new_date = date + relativedelta(months=-ammount)


#-------- Return Name Month


def nombreMeses(mes):
    mes = str(mes)
    if mes == 'Jan' or mes == '01' or mes == '1':
        return('Enero')
    if mes == 'Feb' or mes == '02' or mes == '2':
        return('Febrero')
    if mes == 'Mar' or mes == '03' or mes == '3':
        return('Marzo')
    if mes == 'Apr' or mes == '04' or mes == '4':
        return('Abril')
    if mes == 'May' or mes == '05' or mes == '5':
        return('Mayo')
    if mes == 'Jun' or mes == '06' or mes == '6':
        return('Junio')
    if mes == 'Jul' or mes == '07' or mes == '7':
        return('Julio')
    if mes == 'Aug' or mes == '08' or mes == '8':
        return('Agosto')
    if mes == 'Sep' or mes == '09' or mes == '9':
        return('Septiembre')
    if mes == 'Oct' or mes == '10' or mes == '10':
        return('Octubre')
    if mes == 'Nov' or mes == '11' or mes == '11':
        return('Noviembre')
    if mes == 'Dec' or mes == '12' or mes == '12':
        return('Diciembre')


#------------ FUNCION REEMPLAZAR FECHAS


def ReemplazarFechas(date):
    month = nombreMeses(date[2])
    date[2] = month
    return ' '.join(date)



def format_date_range(list_date):
    date_start = format_date(list_date[0].split('-'), '2')
    date_end = format_date(list_date[1].split('-'), '2')
    format_range = [date_start, date_end]
    return format_range



#------------ FUNCION RETORNAR FECHA ORDENADA


def format_date(date_list, order):
    date_list =  list(map(int, date_list))
    if date_list[1] >= 1 and date_list[1] <= 9:
        date_list[1] = '0' + str(date_list[1])
    if date_list[2] >= 1 and date_list[2] <= 9:
        date_list[2] = '0' + str(date_list[2])
    if order == '1':
        return '{}-{}-{}'.format(date_list[0], date_list[1], date_list[2])
    else:
        return '{}-{}-{}'.format(date_list[2], date_list[1], date_list[0])


#------------ FUNCION RETORNAR FECHA ORDENADA


def fechaList(date):
    date_list = date.strftime('%Y-%d-%m').split('-')
    return date_list


#------------ FUNCCION RETORNA LA CANTIDAD DE DIAS DE UN MES


def days_month(month):
    if month in [2]:
        days = 28
    if month in [4,6,9,11]:
        days = 30
    if month in [1,3,5,7,8,10,12]:
        days = 31   
    return days


#------------ FUNCCION INTERVALO DE FECHAS


def interval_dates(date_start, date_end, month, year):
    interval = {
        'start':'{}-{}-{}'.format(date_start, month, year),
        'end':'{}-{}-{}'.format(date_end, month, year),
    }
    return interval


#------------ FUNCCION RANGO DE FECHAS POR SEMANAS Y MES


def ranges_dates():
    current_date = date.today()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    yerterday = (current_date - relativedelta(days=1))
    last_year = year - 1
    last_month = (current_date - relativedelta(months=+1))
    week_1 = interval_dates(1, 7, month, year)
    week_2 = interval_dates(8, 14, month, year)
    week_3 = interval_dates(15, 21, month, year)
    week_4 = interval_dates(22, days_month(month), month, year)
    current_month = interval_dates(1, days_month(month), month, year)
    last_month = interval_dates(1, days_month(last_month.month), last_month.month, last_month.year)
    yester_day = {'start':'{}-{}-{}'.format(yerterday.day, yerterday.month, yerterday.year), 'end':'{}-{}-{}'.format(yerterday.day, yerterday.month, yerterday.year)}
    current_day = {'start':'{}-{}-{}'.format(day, month, year), 'end':'{}-{}-{}'.format(day, month, year)}
    current_year = {'start':'{}-{}-{}'.format(1, 1, year), 'end':'{}-{}-{}'.format(day, month, year)}
    last_year = {'start':'{}-{}-{}'.format(1, 1, last_year), 'end':'{}-{}-{}'.format(31, 12, last_year)}

    if day in range(1,8):
        week_start = week_1.get('start')
        week_end = week_1.get('end')
    if day in range(8,16):
        week_start = week_2.get('start')
        week_end = week_2.get('end')
    if day in range(16,23):
        week_start = week_3.get('start')
        week_end = week_3.get('end')
    if day in range(23,32):
        week_start = week_4.get('start')
        week_end = week_4.get('end')

    current_week = {'start':week_start, 'end':week_end}

    ranges = {
        'week_1':week_1,
        'week_2':week_2,
        'week_3':week_3,
        'week_4':week_4,
        'yester_day':yester_day,
        'current_day':current_day,
        'current_week':current_week,
        'current_month':current_month,
        'last_month':last_month,
        'current_year':current_year,
        'last_year':last_year,
    }
    return ranges


#------------ FUNCCION RETORNAR FECHAS DEL DASHBOARD


def custom_date_range(filter_dates):
    ranges = ranges_dates()
    date_start = '01-01-2016'
    date_end = ranges.get('current_year').get('end')

    if 'fecha_inicio' in filter_dates:
        date_start = filter_dates.get('fecha_inicio')[0]
    
    if 'fecha_fin' in filter_dates:
        date_end = filter_dates.get('fecha_fin')[0]

    if 'fecha_fin__range' in filter_dates:
        list_range = filter_dates.get('fecha_fin__range')
        date_start = list_range[0]
        date_end = list_range[1]

    ranges['custom_date'] = {'start':str(date_start), 'end':str(date_end)}

    return ranges



def get_date_ranges_request(field_1, field_2, request_filters, range_dates):
    if field_1 in request_filters and field_2 in request_filters:
        date_start = request_filters.get(field_1)[0]
        date_end = request_filters.get(field_2)[0]
    else:
        date_start = range_dates.get('yester_day').get('start')
        date_end = range_dates.get('yester_day').get('end')
        range_dates['custom_date'] = {'start':str(date_start), 'end':str(date_end)}

    list_ranges = format_date_range([date_start, date_end])
    ranges = {'start':list_ranges[0], 'end':list_ranges[1]}
    return ranges



def data_limits_progress(difference, clients_min, contracts_min, appraisals_min):
    difference_days = difference.get('days')
    difference_key = difference.get('key')
    difference_value =  difference.get('value')

    # -- clients
    clients_days = clients_min
    clients_weeks = clients_days * 5
    clients_months = clients_weeks * 4
    clients_years = clients_months * 12

    # -- contracts
    contracts_days = contracts_min
    contracts_weeks = contracts_min
    contracts_months = contracts_weeks * 4
    contracts_years = contracts_months * 12

    # -- appraisals
    appraisals_days = appraisals_min
    appraisals_weeks = appraisals_days * 5
    appraisals_months = appraisals_weeks * 4
    appraisals_years = appraisals_months * 12        
    

    if difference_key == 'days':
        clients_days = clients_days * difference_value
        appraisals_days = appraisals_days * difference_value
    
    if difference_key == 'weeks':
        clients_weeks = clients_weeks * difference_value
        contracts_weeks = contracts_weeks * difference_value
        appraisals_weeks = appraisals_weeks * difference_value
    
    if difference_key == 'months':
        clients_months = clients_months * difference_value
        contracts_months = contracts_months * difference_value
        appraisals_months = appraisals_months * difference_value
    
    if difference_key == 'years':
        clients_years = clients_years * difference_value
        contracts_years = contracts_years * difference_value
        appraisals_years = appraisals_years * difference_value

    clients = {
        'days':clients_days,
        'weeks':clients_weeks,
        'months':clients_months,
        'years':clients_years
    }

    contracts = {
        'days':contracts_days,
        'weeks':contracts_weeks,
        'months':contracts_months,
        'years':contracts_years
    }

    appraisals = {
        'days':appraisals_days,
        'weeks':appraisals_weeks,
        'months':appraisals_months,
        'years':appraisals_years
    }

    data_limits = {
        'clients':clients,
        'contracts':contracts,
        'appraisals':appraisals,
    }

    return data_limits



def difference_dates(date_start_str, date_end_str):
    date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
    date_end = datetime.strptime(date_end_str, '%Y-%m-%d')
    difference_days = date_end - date_start
    days = difference_days.days

    if days <= 9:
        key = 'days'
        value = 1 if days == 0 else 5

    if days >= 10 and days <= 28:
        weeks = int(math.ceil(divide(days, 7)))
        key = 'weeks'
        value = weeks 

    if days >= 29 and days <= 364:
        months = int(math.ceil(divide(days, 31)))
        key = 'months'
        value = months

    if days >= 365:
        years = int(math.ceil(divide(days, 365)))
        key = 'years'
        value = years

    difference = {'key':key, 'value':value}
    
    return difference