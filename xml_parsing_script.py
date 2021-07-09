from xml.etree.ElementTree import parse
import os


courses_list = []

# filename = os.path.join(os.getcwd(), 'xml_files/ugcourse.xml') # file for ug_courses
filename = os.path.join(os.getcwd(), 'xml_files/pgcourse.xml') # file for pg_courses

document = parse(filename)


def parsing_xml(document):
    global courses_list

    for item in document.iterfind('token'):
        for child in item:
            # print(child.attrib["base"])
            courses_list.append(child.attrib["base"])
    
    return courses_list


courses = parsing_xml(document)
print(courses)
