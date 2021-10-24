import PyPDF2

from main.operations.FileUtilities import FileUtilities


class RemovePagesFiles:
    @classmethod
    def remove_pages(cls, file, pages_to_remove):
        actual_filename = file['actual_filename']
        user_filename = file['user_filename']
        reader = PyPDF2.PdfFileReader("storage/"+actual_filename)
        writer = PyPDF2.PdfFileWriter()
        for i in range(reader.numPages):
            if i not in pages_to_remove:
                writer.addPage(reader.getPage(i))
        result_filename = user_filename + " после удаления страниц.pdf"
        FileUtilities.write_pdf(result_filename, writer)
        return result_filename
