import PyPDF2
from django.core.files.storage import FileSystemStorage


class ConcatFiles:
    @staticmethod
    def concat(files):
        merger = PyPDF2.PdfFileMerger()
        resulting_filename = []
        for file in files:
            actual_filename = file['actual_filename']
            merger.append("storage/"+actual_filename)
            user_filename = file['user_filename']
            user_filename = user_filename[0:len(user_filename)-4]
            resulting_filename.append(user_filename)
        resulting_filename_string = "_".join(resulting_filename)
        resulting_filename_string += ".pdf"
        merger.write("storage/"+resulting_filename_string)
        return resulting_filename_string
