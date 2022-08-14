import aspose.words as aw

# load the PDF file
doc = aw.Document("PDF.pdf")

# convert PDF to Word DOCX format
doc.save("pdf-to-word.docx")