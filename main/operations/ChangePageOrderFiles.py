import PyPDF2

from main.operations.FileUtilities import FileUtilities


class ChangePageOrderFiles:
    @classmethod
    def change(cls, files, changes):
        filenames = []
        for change in changes:
            file = cls.get_file(files, change['actual_filename'])
            user_filename = file['user_filename']
            order = change['new_order']
            filenames.append(cls.make_pdf(file['actual_filename'], order, user_filename))
        return filenames

    @classmethod
    def get_file(cls, files, actual_filename):
        for file in files:
            if file['actual_filename'] == actual_filename:
                return file

    @classmethod
    def make_pdf(cls, filename, order, user_filename):
        reader = PyPDF2.PdfFileReader("storage/" + filename)
        writer = PyPDF2.PdfFileWriter()
        numbers = list(order.split("_"))
        for number in numbers:
            if len(number) == 0:
                continue
            index = int(number) - 1
            writer.addPage(reader.getPage(index))
        filename = FileUtilities.generate_tmp_name(FileUtilities.remove_extension(user_filename) + " поменян порядок ", ".pdf")
        FileUtilities.write_pdf(filename, writer)
        return filename
