import re
import en_core_web_lg


nlp = en_core_web_lg.load()

REGEX_LAST_COMPANY = re.compile(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))?\s*([0-9]{4})\s*(to|till|-|–)+\s*(till|Till)?\s*(present|now|current|onward|onwards|date|dates)+\b', re.IGNORECASE)
COMPANY_NAMES_REGEX = re.compile(r'\b[A-Z0-9](?:\w|-)*\s+(?:(?:\w|-)+\s+)*(?:[Ii]nc?|[Ll]td|[Ss]ons)(?:\.|\b)?')
COMPANY_REGEX = re.compile(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))?\s*([0-9]{4})\s*\b(to|till|-|–)+\s*(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember))?\s*([0-9]{4})')

def last_company(professional_segment):
    last_company = ''
    try:
        company_list = []
        all_lines = professional_segment.split('\n')
        for line in all_lines:
            match = re.findall(REGEX_LAST_COMPANY, line)
            # print("match = ",match)
            # print("line = ", line)
            if len(match) != 0:
                match = [i for i in match[0] if i not in ['', ':', ' ']]
                delimiter = ' '.join(match)
                company_list = professional_segment.split(delimiter)[0]
                break
        
        # print("\n\ncompany_list = ", company_list)
        # print(type(company_list))
        
        if company_list:
            # last_company = re.findall(COMPANY_NAMES_REGEX, company_list)
            # last_company = ' '.join(last_company)
            doc = nlp(company_list)
            last_company = [X.text for X in doc.ents if X.label_ == 'ORG']
            # print("\n\n---",last_company)
            if last_company:
                last_company = last_company[0]
            else:
                last_company = ''
            return last_company
        else:
            for line in all_lines:
                match = re.findall(COMPANY_REGEX, line)
                if len(match) != 0:
                    match = [i for i in match[0] if i not in ['', ':', ' ']]
                    delimiter = ' '.join(match)
                    company_list = professional_segment.split(delimiter)[0]
                    break
            # print("\n\n----company list = ",company_list)

            if company_list:
                # last_company = re.findall(COMPANY_NAMES_REGEX, company_list)
                # last_company = ' '.join(last_company)
                doc = nlp(company_list)
                last_company = [X.text for X in doc.ents if X.label_ == 'ORG']
                # print("\n\n$$$$",last_company)
                if last_company:
                    last_company = last_company[0]
                else:
                    last_company = ''
                return last_company
            else:
                # print("\n\n***",last_company)
                return last_company


    except Exception as e:
        last_company = ''
        print("error occurred in extracting last company")
        return last_company
