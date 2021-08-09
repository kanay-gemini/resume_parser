import subprocess
import os

# output_dir = os.path.join(os.getcwd(), 'sample_resumes/')

# filename = os.path.join(os.getcwd(), 'sample_resumes/Lakhvir_Bansal_Resume.doc')

def doc_to_docx(filename, output_dir):
    subprocess.call(["libreoffice", "--headless", "--convert-to", "docx", "--outdir", output_dir, filename])
    filename = filename[0:-4] + ".docx"
    print(filename)
    return filename


# doc_to_docx(filename)