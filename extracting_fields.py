from resume_segmentation import personal_segment, education_segment, professional_segment, skills_segment
import re
import spacy
from spacy.matcher import Matcher
import nltk
from nltk.corpus import stopwords
import csv
from data import synonym_dict


PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')


def extract_phone_number(personal_segment):
    phone = re.findall(PHONE_REG, personal_segment)
    if phone:
        number = ''.join(phone[0])

        if personal_segment.find(number) >= 0 and len(number) < 16:
            return number
    return None


mobile_number = extract_phone_number(personal_segment)
print("mobile number = ", mobile_number)


def extract_emails(personal_segment):
    return re.findall(EMAIL_REG, personal_segment)[0]


email = extract_emails(personal_segment)
print("email = ", email)


# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):

    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text


name = extract_name(personal_segment)
print("name = ", name)


# GRADUATION_REGEX = re.compile(r'\d{4}-\d{4}')


# def extract_graduation_year(text):
#     return re.findall(GRADUATION_REGEX, text)


# graduation_year = extract_graduation_year(education_segment)
# print("graduation_year = ", graduation_year)



def extract_ug_course(education_segment):
    ug_course = ''
    for element in synonym_dict["ug_courses"]:
        if re.search(r'\b' + element + r'\b', education_segment):
            ug_course = element
            break
        # if element in education_segment:
        #     ug_course = element
        #     print(ug_course)
    return ug_course


ug_course = extract_ug_course(education_segment)
print("ug_course = ", ug_course)


def extract_pg_course(education_segement):
    pg_course = ''
    for element in synonym_dict["pg_courses"]:
        if re.search(r'\b' + element + r'\b', education_segment):
            pg_course = element
            break
    return pg_course


pg_course = extract_pg_course(education_segment)
print("pg_course = ", pg_course)



new_line=""
def grad_education(education_segment):
    global new_line
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
                new_line=educations[i+1]
            break
    return ans

ans=grad_education(education_segment)
# print("------",ans,"------")
YEAR_REG=re.compile(r'\d{4}')
def grad_year(text):
    return re.findall(YEAR_REG, text)
year=grad_year(ans)
print("Grad year",year)

years="".join(year)
nans=ans.replace(ug_course," ")
nnans=nans.replace(years," ")
try:
    college=nnans.split("from",1)[1]
    print("College name->",nnans.split("from",1)[1])
except:
    print(new_line)
