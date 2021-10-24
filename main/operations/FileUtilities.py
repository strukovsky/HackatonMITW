import random


class FileUtilities:

    @classmethod
    def remove_extension(cls, filename):
        if len(filename) < 4:
            return filename
        if filename[len(filename) - 4:] == ".pdf":
            filename = filename[:len(filename) - 4]
        return filename

    @classmethod
    def write_pdf(cls, filename, pdf_writer):
        with open("storage/" + filename, "wb") as output:
            pdf_writer.write(output)

    @classmethod
    def generate_tmp_name(cls, prefix, extension):
        filename = prefix
        filename += "".join(random.choices("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", k=6))
        filename += extension
        return filename
