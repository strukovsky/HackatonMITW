import PyPDF2

from main.operations.FileUtilities import FileUtilities


class RotateFiles:

    def __init__(self):
        self.filenames = []

    def rotate(self, files, degrees):
        for file in files:
            actual_name = file['actual_filename']
            user_name = file['user_filename']
            image = file['image']
            self.perform_rotation(user_name, int(degrees))
        return self.filenames

    def perform_rotation(self, file, degrees):
        reader = PyPDF2.PdfFileReader("storage/"+file)
        writer = PyPDF2.PdfFileWriter()
        for i in range(reader.numPages):
            page = reader.getPage(i)
            page.rotateClockwise(degrees)
            writer.addPage(page)
        filename = file + " повернут на " + str(degrees) + " по часовой.pdf"
        FileUtilities.write_pdf(filename, writer)
        self.filenames.append(filename)
