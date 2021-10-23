from main.operations.OperationTemplateInfo import OperationTemplateInfo


class MapOperation:
    @staticmethod
    def map(operation_type):
        if operation_type == "concat":
            return OperationTemplateInfo("concat", "Соединить файлы!")
        if operation_type == "split":
            return OperationTemplateInfo("split", "Разбить файл(ы)!")
