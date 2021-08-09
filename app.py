import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from resume_segmentation import document_object, properties_identifier, bold_headings, h1_headings, h2_headings, h3_headings, font_size, font_color, maximum_headings, resume_headings, extract_text_from_doc, customized_headers, text_between_various_headings

from data import synonym_dict
from extracting_fields import extract_phone_number, extract_emails, extract_name, extract_ug_course, \
    extract_pg_course, ug_education, grad_year, ug_college, pg_education, post_grad_year, pg_college
from experience_file import experience
from extract_last_company import last_company
import time
from doc_to_docx import doc_to_docx

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_resumes')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'docx', 'doc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SECRET_KEY=os.urandom(30))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extracted_fields(name=None, email=None, phone=None, ug_degree=None, ug_year=None, ug_clg=None, pg_degree=None, pg_year=None, pg_clg=None, last_company=None, exp=None):
    result = {
        "Name": None,
        "Email": None,
        "Phone": None,
        "UG Degree": None,
        "UG Year": None,
        "UG College": None,
        "PG Degree": None,
        "PG Year": None,
        "PG College": None,
        "Last Company": None,
        "Experience": None
    }

    result.update({
        "Name": name,
        "Email": email,
        "Phone": phone,
        "UG Degree": ug_degree,
        "UG Year": ug_year,
        "UG College": ug_clg,
        "PG Degree": pg_degree,
        "PG Year": pg_year,
        "PG College": pg_clg,
        "Last Company": last_company,
        "Experience": exp
    })

    return result


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    result = {
        "message": None
    }
    if request.method == "POST":
        try:
            if 'files' not in request.files:
                flash('No resume found')
                result.update({
                    "message": "No resume found"
                })
                return redirect(url_for('home'))
            files = request.files.getlist('files')
            
            resultant_list = []
            for file in files:

                if file.filename == "":
                    flash("No selected resume")
                    result.update({
                        "message": "No resume selected"
                    })
                    return redirect(url_for('home'))
                if file and allowed_file(file.filename):
                    bold = []
                    h1 = []
                    h2 = []
                    h3 = []
                    h4 = []
                    italic = []
                    color_dict = {}
                    color_size_dict={}
                    font_dict = {}
                    font_size_dict = {}
                    HEADERS_OF_RESUME = []
                    font_dict_header = []
                    color_dict_header = []
                    count_size = 0
                    count_color = 0
                    filename = secure_filename(file.filename)
                    # print("filename = ", filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    if filename.endswith('doc'):
                        filename = doc_to_docx(filename, app.config['UPLOAD_FOLDER'])
                        print(filename)

                    document = document_object(filename)

                    properties = properties_identifier(document)
                    bold = properties[0]
                    italic = properties[1]
                    h1 = properties[2]
                    h2 = properties[3]
                    h3 = properties[4]
                    h4 = properties[5]
                    color_dict = properties[6]
                    color_size_dict = properties[7]
                    font_dict = properties[8]
                    font_size_dict = properties[9]

                    # time.sleep(1)

                    
                    # print("bold data = ", bold)
                    # print("italic data = ", italic)
                    # print("Heading 1 = ", h1)
                    # print("Heading 2 = ", h2)
                    # print("Heading 3 = ", h3)
                    # print("color dict = ", color_dict)
                    # print("font dict = ", font_dict)
                    # print("color_size_dict = ", color_size_dict)
                    # print("font_size_dict= ",font_size_dict)

                    no_of_headings_in_bold = bold_headings(bold, synonym_dict)
                    no_of_headings_in_h1 = h1_headings(h1, synonym_dict)
                    no_of_headings_in_h2 = h2_headings(h2, synonym_dict)
                    no_of_headings_in_h3 = h3_headings(h3, synonym_dict)
                    no_of_headings_in_font_size, font_dict_header = font_size(font_dict, synonym_dict)
                    no_of_headings_in_color, color_dict_header = font_color(color_dict, synonym_dict)

                    maximum = maximum_headings(no_of_headings_in_bold, no_of_headings_in_h1, no_of_headings_in_h2, no_of_headings_in_h3, no_of_headings_in_font_size, no_of_headings_in_color)
                    
                    HEADERS_OF_RESUME = resume_headings(maximum, no_of_headings_in_bold, no_of_headings_in_h1, no_of_headings_in_h2, no_of_headings_in_h3, no_of_headings_in_font_size, no_of_headings_in_color, bold, h1, h2, h3, font_dict_header, color_dict_header)
                    
                    complete_page_text = extract_text_from_doc(filename)
                    
                    HEADERS_OF_RESUME = customized_headers(HEADERS_OF_RESUME, synonym_dict, complete_page_text)
                    
                    career_objective_segment, personal_segment, education_segment, skills_segment, professional_segment= text_between_various_headings(complete_page_text, synonym_dict, HEADERS_OF_RESUME)
                    # time.sleep(1)

                    name = extract_name(personal_segment)
                    email = extract_emails(personal_segment)
                    mobile_number = extract_phone_number(personal_segment)
                    ug_course = extract_ug_course(education_segment)
                    pg_course = extract_pg_course(education_segment)

                    ug_line = ug_education(education_segment, ug_course)
                    ug_year = grad_year(ug_line)
                    ug_clg_name = ug_college(ug_course, ug_line, ug_year)
                    pg_line = pg_education(education_segment, pg_course)
                    pg_year = post_grad_year(pg_line)
                    pg_clg_name = pg_college(pg_course, pg_line, pg_year)
                    exp = experience(professional_segment)
                    company_name = last_company(professional_segment)
                    
                    time.sleep(1)

                    result = get_extracted_fields(name=name, email=email, phone=mobile_number, ug_degree=ug_course, pg_degree=pg_course, last_company=company_name, exp=exp, ug_year=ug_year, pg_year=pg_year, ug_clg=ug_clg_name, pg_clg=pg_clg_name)
                    resultant_list.append(result)

            return render_template("result.html", resultant_list=resultant_list)
        except Exception as e:
            print(e)
            result.update({
                "message": "error occurred"
            })
            return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
