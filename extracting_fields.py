import re
import spacy
from spacy.matcher import Matcher
from data import synonym_dict


PHONE_REG = re.compile(r'\+?[0-9 \-]+?[0-9]{8,}')
EMAIL_REG = re.compile(r'[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
DATE_REG = re.compile(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)) ([0-9]{4})')
dict={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Sept":9,"Oct":10,"Nov":11,"Dec":12,"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
YEAR_REG=re.compile(r'\d{4}')

def extract_phone_number(personal_segment):
    try:
        phone = ''
        phone = re.findall(PHONE_REG, personal_segment)
        if phone:
            number = ''.join(phone[0])

            if personal_segment.find(number) >= 0 and len(number) < 16:
                return number
        return None
    except Exception as e:
        print("error occured in finding phone number")
        return phone


def extract_emails(personal_segment):
    email = ''
    try:
        email =  re.findall(EMAIL_REG, personal_segment)
        if email:
            return email[0]
        else:
            email = re.findall(re.compile(r'[a-zA-Z0-9\.\-+_]+@?[a-z0-9\.\-+_]+\.[a-z]+'),personal_segment)
            if email:
                return email[0]
            else:
                raise Exception
    except Exception as e:
        email = ''
        print("error occured in finding email")
        return email


def extract_name(resume_text):
    name = ''
    try:
        # load pre-trained model
        nlp = spacy.load('en_core_web_sm')

        # initialize matcher with a vocab
        matcher = Matcher(nlp.vocab)

        nlp_text = nlp(resume_text)

        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

        matcher.add('NAME', [pattern])

        matches = matcher(nlp_text)

        name_list = []
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            name_list.append(span.text)
        false_word_list = ['curriculum vitae', 'CURRICULUM VITAE', 'Curriculum Vitae', 'resume', 'RESUME', 'Resume']
        for word in false_word_list:
            if word in name_list:
                name_list.remove(word)
        name = name_list[0]
        return name
    except Exception as e:
        name = ''
        print("error occured in finding name")
        return name


def extract_ug_course(education_segment):
    try:
        ug_course = ''
        for element in synonym_dict["ug_courses"]:
            if re.search(r'\b' + element + r'\b', education_segment):
                ug_course = element
                break
        return ug_course
    except Exception as e:
        ug_course = ''
        print("error occur in finding ug course")
        return ug_course


# ug_course = extract_ug_course(education_segment)


def extract_pg_course(education_segment):
    try:
        pg_course = ''
        for element in synonym_dict["pg_courses"]:
            if re.search(r'\b' + element + r'\b', education_segment):
                pg_course = element
                break
        return pg_course
    except Exception as e:
        # pg_course = ''
        print("error occured in finding pg course")
        return pg_course


def ug_education(education_segment, ug_course):
    ug_line=""
    ans = ''
    try:
        educations=education_segment.split('\n')
        for i in range(len(educations)):
            if ug_course in educations[i]:
                ans=educations[i]
                flag=1
                not_ug_course = []
                not_ug_course = synonym_dict["pg_courses"] + synonym_dict["matrix"]
                for elem in not_ug_course:
                    if elem in educations[i+1]:
                        flag=0
                        break
                if flag==1:
                    ans+=" "+educations[i+1]
                    ug_line=educations[i+1]
                break
        return ans
    except Exception as e:
        ans = ''
        print("error occur in finding ug_line")
        return ans


def grad_year(text):
    try:
        year_of_graduation = ''
        graduation_year =  re.findall(YEAR_REG, text)
        if len(graduation_year) == 2:
            year_of_graduation = graduation_year[0] + "-" + graduation_year[1]
        elif len(graduation_year) == 1:
            year_of_graduation = graduation_year[0]
        else:
            year_of_graduation = ''
        return year_of_graduation
    except Exception as e:
        year_of_graduation = ''
        return year_of_graduation


def ug_college(ug_course, ug_line, ug_year):
    try:
        years="".join(ug_year)
        nans=ug_line.replace(ug_course," ")
        nnans=nans.replace(years," ")
        college=nnans.split("from",1)[1]
        # print("UG college = ",nnans.split("from",1)[1])
        return college
    except:
        # print("UG college = ", ug_line)
        return ug_line


def pg_education(education_segment, pg_course):
    pg_line=""
    ans = ''
    try:
        educations=education_segment.split('\n')
        for i in range(len(educations)):
            if pg_course in educations[i]:
                ans=educations[i]
                flag=1
                not_pg_course = []
                not_pg_course = synonym_dict["ug_courses"] + synonym_dict["matrix"]
                for elem in not_pg_course:
                    if elem in educations[i+1]:
                        flag=0
                        break
                if flag==1:
                    ans+=" "+educations[i+1]
                    pg_line=educations[i+1]
                break
        return ans
    except Exception as e:
        print("error occur in finding pg_line")
        return ans


def post_grad_year(text):
    try:
        year_of_post_graduation = ''
        graduation_year =  re.findall(YEAR_REG, text)
        if len(graduation_year) == 2:
            year_of_post_graduation = graduation_year[0] + "-" + graduation_year[1]
        elif len(graduation_year) == 1:
            year_of_post_graduation = graduation_year[0]
        else:
            year_of_post_graduation = ''
        return year_of_post_graduation
    except Exception as e:
        year_of_post_graduation = ''
        return year_of_post_graduation


def pg_college(pg_course, pg_line, pg_year):
    try:
        years="".join(pg_year)
        nans=pg_line.replace(pg_course," ")
        nnans=nans.replace(years," ")
        college=nnans.split("from",1)[1]
        # print("PG college = ",nnans.split("from",1)[1])
        return college
    except:
        # print("PG college = ", pg_line)
        return pg_line
