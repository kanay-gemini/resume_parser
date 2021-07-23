from resume_segmentation import personal_segment, education_segment, professional_segment, skills_segment
import re
import spacy
from spacy.matcher import Matcher
import nltk
from nltk.corpus import stopwords
import csv
from data import synonym_dict


PHONE_REG = re.compile(r'\+?[0-9 \-]+?[0-9]{8,}')
EMAIL_REG = re.compile(r'[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')


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


mobile_number = extract_phone_number(personal_segment)
print("mobile number = ", mobile_number)


def extract_emails(personal_segment):
    try:
        email = ''
        email =  re.findall(EMAIL_REG, personal_segment)[0]
        return email
    except Exception as e:
        return re.findall(re.compile(r'[a-zA-Z0-9\.\-+_]+@?[a-z0-9\.\-+_]+\.[a-z]+'),personal_segment)


email = extract_emails(personal_segment)
print("email = ", email)


# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    try:
        nlp_text = nlp(resume_text)

        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

        matcher.add('NAME', [pattern])

        matches = matcher(nlp_text)

        name_list = []
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            name_list.append(span.text)
        return name_list[0]
    except Exception as e:
        print("error occured in finding name")
        return name_list

name = extract_name(personal_segment)
print("name = ", name)


# GRADUATION_REGEX = re.compile(r'\d{4}-\d{4}|\d{4}')


# def extract_graduation_year(text):
#     return re.findall(GRADUATION_REGEX, text)


# graduation_year = extract_graduation_year(education_segment)
# print("graduation_year = ", graduation_year)



def extract_ug_course(education_segment):
    try:
        ug_course = ''
        for element in synonym_dict["ug_courses"]:
            if re.search(r'\b' + element + r'\b', education_segment):
                ug_course = element
                break
        return ug_course
    except Exception as e:
        print("error occur in finding ug course")
        return ug_course


ug_course = extract_ug_course(education_segment)


def extract_pg_course(education_segement):
    try:
        pg_course = ''
        for element in synonym_dict["pg_courses"]:
            if re.search(r'\b' + element + r'\b', education_segment):
                pg_course = element
                break
        return pg_course
    except Exception as e:
        print("error occured in finding pg course")
        return pg_course


pg_course = extract_pg_course(education_segment)


ug_line=""
def ug_education(education_segment):
    global ug_line
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
        print("error occur in finding ug_line")
        return ans

ans=ug_education(education_segment)
# print("------",ans,"------")
YEAR_REG=re.compile(r'\d{4}')
def grad_year(text):
    return re.findall(YEAR_REG, text)
year=grad_year(ans)
print("UG degree = ",ug_course)
print("UG year = ",year)

years="".join(year)
nans=ans.replace(ug_course," ")
nnans=nans.replace(years," ")
try:
    college=nnans.split("from",1)[1]
    print("UG college = ",nnans.split("from",1)[1])
except:
    print("UG college = ", ans)

pg_line=""
def pg_education(education_segment):
    global pg_line
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

ans=pg_education(education_segment)
YEAR_REG=re.compile(r'\d{4}')
def grad_year(text):
    return re.findall(YEAR_REG, text)
year=grad_year(ans)
print("PG degree = ",pg_course)
print("PG year = ",year)

years="".join(year)
nans=ans.replace(ug_course," ")
nnans=nans.replace(years," ")
try:
    college=nnans.split("from",1)[1]
    print("PG college = ",nnans.split("from",1)[1])
except:
    print("PG college = ", ans)



# def extract_college(education_segment):
#     college = ''
#     education_segment = ' '.join([i.lower() for i in education_segment.split(' ')])
#     # education_segment = "dev bhoomi institute of technology"
#     print("Education segment = ", education_segment)
#     # print(type(education_segment))
#     for institute in synonym_dict["institutes"]:
#         # if re.search(r'\b' + institute + r'\b', education_segment, re.IGNORECASE):
#         #     college = institute
#         #     break
#         if institute in education_segment:
#             college = institute
#             # print(institute)
#     return college

# print(extract_college(ans))
