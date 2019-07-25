import tkinter
import tkinter.filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import eel
import os


eel.init('web')

@eel.expose
def get_number_of_pages(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        print(number_of_pages)
        return number_of_pages


@eel.expose
def btn_ResimyoluClick():
    "get full path of file"
    root = tkinter.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    path = tkinter.filedialog.askopenfile(filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    return path.name


@eel.expose
def split(pdf_file, start_page, end_page):
    start_page, end_page = int(start_page), int(end_page)
    input_pdf = PdfFileReader(open(pdf_file, 'rb'))
    output_pdf = PdfFileWriter()
    # name it
    new_name = rename_file(pdf_file, '_splited')
    # creet blank file
    new_file = open(new_name, 'wb')
    # insert pages in blank file
    while start_page <= end_page:
        output_pdf.addPage(input_pdf.getPage(start_page))
        output_pdf.write(new_file)
        start_page += 1
    # close it
    new_file.close()


@eel.expose
def merge(pdf_file1, pdf_file2):
    pdf_merger = PdfFileMerger()
    pdf_merger.append(pdf_file1)
    pdf_merger.append(pdf_file2)

    new_file = rename_file(pdf_file1, '_merged')
    with open(new_file, 'wb') as fileobj:
        pdf_merger.write(fileobj)


@eel.expose
def crop(pdf_file, top, right, bottom, left):
    input_pdf = PdfFileReader(open(pdf_file, 'rb'))
    output_pdf = PdfFileWriter()
    top, right, bottom, left = int(top), int(right), int(bottom), int(left)

    new_name = rename_file(pdf_file, '_croped')
    new_file = open(new_name, 'wb')

    num_pages = input_pdf.getNumPages()

    for i in range(num_pages):
        page = input_pdf.getPage(i)

        page.mediaBox.upperRight = (page.mediaBox.getUpperRight_x() - right, page.mediaBox.getUpperRight_y() - top)
        page.mediaBox.lowerLeft  = (page.mediaBox.getLowerLeft_x()  + left,  page.mediaBox.getLowerLeft_y()  + bottom)

        output_pdf.addPage(page)
        output_pdf.write(new_file)
    
    new_file.close()


def rename_file(pdf_file, refrain):
    """ return new name width _splited
        >>> rename_file(file.pdf, "_splited") -> file_splited.pdf
        if file_splited.pdf existe -> file_splited_1.pdf
        ....
    """
    new_name = pdf_file[:-4] + f"{refrain}.pdf"
    i = 1
    while os.path.isfile(new_name):
        new_name = pdf_file[:-4] + f"{refrain}_{i}.pdf"
        i +=1
    return new_name


eel.start('index.html', size=(475, 712))
