import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import docx2txt
from data import synonym_dict


level_from_style_name = {f'Heading {i}': f'<H{i}>' for i in range(10)}


filename = '/home/kanay/Documents/sample.docx'

d = docx.Document(filename)

headings_in_resumes = []

career_objective_segment = ''
personal_segment = ''
education_segment = ''
professional_segment = ''
skills_segment = ''

full_text = []
bold = []
h1 = []
h2 = []
h3 = []
h4 = []
italic = []
normal = []
body_text = []
colors = []
color_dict = {}
font_dict = {}
font_size_dict = {}


rels = d.part.rels


for para in d.paragraphs:
    if para.style.name not in level_from_style_name:
        if para.style.name == "Normal":
            normal.append(para.text)
        if para.style.name == "Body Text":
            body_text.append(para.text)
        full_text.append(para.text)
    else:
        level = level_from_style_name[para.style.name]
        if level == "<H1>":
            h1.append(para.text)
        if level == "<H2>":
            h2.append(para.text)
        if level == "<H3>":
            h3.append(para.text)
        if level == "<H4>":
            h4.append(para.text)

    for run in para.runs:
        if run.bold:
            bold.append(run.text)
        if run.italic:
            italic.append(run.text)
        if run.font.color.rgb is not None:
            colors.append(run.font.color.rgb)
            # print("colors = ", colors)

    for run in para.runs:
        if run.font.color.rgb is not None:
            if run.font.color.rgb in color_dict:
                color_dict[run.font.color.rgb].append(run.text)
            else:
                color_dict[run.font.color.rgb] = [run.text]

        if run.font.size is not None:
            if run.font.size in font_dict:
                font_dict[run.font.size].append(run.text)
            else:
                font_dict[run.font.size] = [run.text]
                # print("font size = " + str(run.font.size) + " = " + run.text)

        if run.font.size is not None:
            if run.font.size in font_size_dict:
                font_size_dict[run.font.size] += 1
            else:
                font_size_dict[run.font.size] = 1


print("\n\n")

print("bold data = ", bold)
print("italic data = ", italic)
print("Heading 1 = ", h1)
print("Heading 2 = ", h2)
print("Heading 3 = ", h3)
print("Heading 4 = ", h4)
print("color dict = ", color_dict)
print("font dict = ", font_dict)
print("\n\nfont_size_dict = ", font_size_dict)


HEADERS_OF_RESUME = []
header_count = 0
no_of_headings_in_bold = 0
for heading in synonym_dict["main_headings"]:
    if heading in [i.lower() for i in bold]:
        no_of_headings_in_bold += 1
print("no_of_headings_in_bold = ", no_of_headings_in_bold)


no_of_headings_in_h1 = 0
for heading in synonym_dict["main_headings"]:
    if heading in [i.lower() for i in h1]:
        no_of_headings_in_h1 += 1
print("no_of_headings_in_h1 = ", no_of_headings_in_h1)

no_of_headings_in_h2 = 0
for heading in synonym_dict["main_headings"]:
    if heading in [i.lower() for i in h2]:
        no_of_headings_in_h2 += 1
print("no_of_headings_in_h2 = ", no_of_headings_in_h2)

no_of_headings_in_h3 = 0
for heading in synonym_dict["main_headings"]:
    if heading in [i.lower() for i in h3]:
        no_of_headings_in_h3 += 1
print("no_of_headings_in_h3 = ", no_of_headings_in_h3)


count = 0
no_of_headings_in_font_size = 0
font_dict_header = []

for values_list in list(font_dict.values()):
    for heading in synonym_dict["main_headings"]:
        if heading in [i.lower() for i in values_list]:
            no_of_headings_in_font_size += 1
            if no_of_headings_in_font_size > count:
                count = no_of_headings_in_font_size
                font_dict_header = values_list
print("no_of_headings_in_font_size = ", no_of_headings_in_font_size)

header_list_count = [no_of_headings_in_bold, no_of_headings_in_h1,
                     no_of_headings_in_h2, no_of_headings_in_h3, count]
maximum = max(header_list_count)

if no_of_headings_in_bold == maximum:
    HEADERS_OF_RESUME = bold
elif no_of_headings_in_h1 == maximum:
    HEADERS_OF_RESUME = h1
elif no_of_headings_in_h2 == maximum:
    HEADERS_OF_RESUME = h2
elif no_of_headings_in_h3 == maximum:
    HEADERS_OF_RESUME = h3
elif count == maximum:
    HEADERS_OF_RESUME = font_dict_header
else:
    pass


print("HEADERS_OF_RESUME = ", HEADERS_OF_RESUME)


# def extract_text_from_doc(filename):
#     d = docx.Document(filename)
#     complete_text = []
#     for para in d.paragraphs:
#         complete_text.append(para.text)
#     return '\n'.join(complete_text)

def extract_text_from_doc(filename):
    temp = docx2txt.process(filename)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return '\n'.join(text)

complete_page_text = extract_text_from_doc(filename)


def text_between_various_headings():
    length = len(HEADERS_OF_RESUME)
    global career_objective_segment
    global personal_segment
    global education_segment
    global professional_segment
    global skills_segment

    personal_segment = complete_page_text.split(HEADERS_OF_RESUME[0])[0]


    # print("personal segment = {}".format(personal_segment))
    for i in range(length-1):
        if HEADERS_OF_RESUME[i].lower() in synonym_dict["career_objective"]:
            career_objective_segment = complete_page_text.split(
                HEADERS_OF_RESUME[i])[1].split(HEADERS_OF_RESUME[i+1])[0]
        elif HEADERS_OF_RESUME[i].lower() in synonym_dict["education"]:
            education_segment = complete_page_text.split(HEADERS_OF_RESUME[i])[1].split(HEADERS_OF_RESUME[i+1])[0]
        elif HEADERS_OF_RESUME[i].lower() in synonym_dict["professional_experience"]:
            professional_segment = complete_page_text.split(HEADERS_OF_RESUME[i])[1].split(HEADERS_OF_RESUME[i+1])[0]
        elif HEADERS_OF_RESUME[i].lower() in synonym_dict["skills"]:
            skills_segment = complete_page_text.split(HEADERS_OF_RESUME[i])[1].split(HEADERS_OF_RESUME[i+1])[0]
        else:
            pass

text_between_various_headings()


print("personal_segment = ", personal_segment)
print("career_objective_segment = ",career_objective_segment)
print("education_segment = ", education_segment)
print("skills_segment = ", skills_segment)
print("professional_segment = ", professional_segment)
