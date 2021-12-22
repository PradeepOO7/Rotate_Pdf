import os
from flask import Flask, jsonify, request
import PyPDF2
from pathlib import Path 
from datetime import datetime
#function to rotate pdf pages
def rotatepdf(path,n,angle):
    pdf_in = open(path, 'rb')
    angle=int(angle)
    path=Path(path).name.replace('.pdf','')
    path=os. getcwd().replace("\\","/")+'/Rotated_pdf/'+path+datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'.pdf'
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()  
    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        if pagenum==int(n)-1:
            page.rotateClockwise(angle)
        pdf_writer.addPage(page)
    pdf_out = open(path, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()
    return path
#initializing flask app
app= Flask(__name__)
@app.route("/rotatepdf", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()
        path=rotatepdf(posted_data['file_path'],posted_data['page_number'],posted_data['angle_of_rotation'])
        return jsonify({"file_path":path})

if __name__=='__main__':
    app.run()