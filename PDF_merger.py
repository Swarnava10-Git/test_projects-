import PyPDF2

pdf1=input('enter main pdf name:')
input_pdf = PyPDF2.PdfReader(open(pdf1, 'rb'))

pdf2=input('enter sub pdf name:')
stamp = PyPDF2.PdfReader(open(pdf2, 'rb')).pages[0]

output_pdf = PyPDF2.PdfWriter()

for i in range(len(input_pdf.pages)):
    page = input_pdf.pages[i]
    
    page.merge_page(stamp)
    
    output_pdf.add_page(page)

with open('output_file.pdf', 'wb') as f:
    output_pdf.write(f)
print()
print('Success!')
a=str(input(''))
