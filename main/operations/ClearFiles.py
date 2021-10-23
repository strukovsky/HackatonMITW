from django.core.files.storage import FileSystemStorage


class ClearFiles:

    @staticmethod
    def clear(files):
        fs = FileSystemStorage()
        for file in files:
            actual_filename = file['actual_filename']
            image = file['image']
            fs.delete(actual_filename)
            fs.delete(image)
