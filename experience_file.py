import re
from datetime import date


REGEX_EXP = re.compile(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))?\s*([0-9]{4})\b', re.IGNORECASE)
dict={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Sept":9,"Oct":10,"Nov":11,"Dec":12,"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}


month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sept?",10:"Oct",11:"Nov",12:"Dec"}
def find_month_year():
    todays_date = date.today()
    month = todays_date.month
    year = todays_date.year
    # print(month)
    mon_year_tup = (month_dict[month], year)
    # print(mon_year_tup)
    return mon_year_tup


def experience(professional_segment):
    exp = 0
    try:
        REG_FOR_TILL_DATE = re.compile(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))?\s*([0-9]{4})\s*(to|till|-)+\s*(till)?\s*(present|now|current|onward|onwards|date|dates)+\b', re.IGNORECASE)
        all_lines=professional_segment.split('\n')
        experience_list = []
        exp_till_date = []
        for line in all_lines:
            year=re.findall(REGEX_EXP, line)
            if len(year) != 0:
                experience_list.append(year)
            year_in_till_date = re.findall(REG_FOR_TILL_DATE, line)
            if len(year_in_till_date) != 0:
                exp_till_date.append(year_in_till_date)
        # print(experience_list)
        # print(exp_till_date)
        months=0
        for experience in experience_list:
            if len(experience)==2:
                # print(experience[0],experience[1])
                if experience[0][0] != '' and experience[1][0] != '':
                    if dict[experience[0][0]]<=dict[experience[1][0]]:
                        months+=(int(experience[1][1])-int(experience[0][1]))*12 + (dict[experience[1][0]]-dict[experience[0][0]])
                    else:
                        months+=(int(experience[1][1])-int(experience[0][1]))*12 - (dict[experience[0][0]]-dict[experience[1][0]])
                else:
                    months += (int(experience[1][1]) - int(experience[0][1]))*12
        for experience in exp_till_date:
            if len(experience)!=0:
                month_year = find_month_year()
                if experience[0][0] != '':
                    if dict[experience[0][0]]<=dict[month_year[0]]:
                        months+=(int(month_year[1])-int(experience[0][1]))*12 + (dict[month_year[0]]-dict[experience[0][0]])
                    else:
                        months+=(int(month_year[1])-int(experience[0][1]))*12 - (dict[experience[0][0]]-dict[month_year[0]])
                else:
                    months+=(int(month_year[1])-int(experience[0][1]))*12
        
        exp = months/12

        if exp != 0 or exp != 0.0:
            exp = "{:.2f}".format(exp)            
            return exp
        else:
            EXP_REGEX = re.compile(r'([0-9]+\.?[0-9]{0,3}\s?y[ears|ear|rs|r]+\s?[0-9]{0,2}\s?[months|month]?)')
            experience_list = []
            all_lines = professional_segment.split('\n')
            for line in all_lines:
                # print(line)
                year = []
                year = re.findall(EXP_REGEX, line)
                experience_list.append(year)
            exp = 0
            # print(experience_list)
            for experience in experience_list:
                if experience:
                    years = experience[0].split()
                    if len(years) < 4:
                        exp += float(years[0])
                    else:
                        exp = (exp + float(years[0])*12 + float(years[2]))/12
            exp = "{:.2f}".format(exp)
            return exp
    except Exception as e:
        print("error in extracting experience")
        return exp
