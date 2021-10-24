from pdf2image import pdf2image

from main.operations.FileUtilities import FileUtilities


class PreparePagesOfFiles:
    @classmethod
    def prepare(cls, files):
        result = []
        for file in files:
            actual_name = file['actual_filename']
            user_name = file['user_filename']
            pages = cls.build_images(user_name, actual_name)
            result.append({
                "actual_filename": actual_name,
                "user_filename": user_name,
                "pages": pages['result'],
                "pages_count": pages['pages_count']
            })
        return result

    @classmethod
    def build_images(cls, user_filename, actual_filename):
        user_filename = FileUtilities.remove_extension(user_filename)
        images = pdf2image.convert_from_path("storage/" + actual_filename)
        page_iteration = 1
        pages_total = 0
        result = []
        for image in images:
            image_filename = user_filename + " страница " + str(page_iteration) + ".jpg"
            image.save("storage/" + image_filename)
            result.append({
                "image": image_filename,
                "number": page_iteration
            })
            page_iteration += 1
            pages_total += 1

        return {
            "result": result,
            "pages_count": pages_total
        }
