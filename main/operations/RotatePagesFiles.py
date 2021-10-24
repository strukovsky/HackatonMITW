import PyPDF2

from main.operations.FileUtilities import FileUtilities


class RotatePagesFiles:
    @classmethod
    def rotate(cls, file, rotation):
        actual_filename = file['actual_filename']
        user_filename = file['user_filename']
        reader = PyPDF2.PdfFileReader("storage/" + actual_filename)
        writer = PyPDF2.PdfFileWriter()
        for i in range(reader.numPages):
            page = reader.getPage(i)
            for elem in rotation:
                page_number = elem['page_number']
                degrees = elem['degrees']
                if degrees == 0:
                    continue
                if page_number == i:
                    page.rotateClockwise(degrees)
            writer.addPage(page)
        result_filename = user_filename + " после вращения страниц.pdf"
        FileUtilities.write_pdf(result_filename, writer)
        return result_filename
