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


GRADUATION_REGEX = re.compile(r'\d{4}-\d{4}')


def extract_graduation_year(text):
    return re.findall(GRADUATION_REGEX, text)


graduation_year = extract_graduation_year(education_segment)
print("graduation_year = ", graduation_year)


def extract_college(education_segment):
    college = ''
    education_segment = ' '.join([i.lower() for i in education_segment.split(' ')])
    # print("Education segment = ", education_segment)
    # print(type(education_segment))
    for institute in synonym_dict["institutes"]:
        # if re.search(institute, education_segment):
        #     college = institute
        #     break
        if institute in education_segment:
            college = institute
            # college = education_segment
            print(institute)
    return college

print(extract_college(education_segment))
