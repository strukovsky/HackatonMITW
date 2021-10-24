from main.operations.OperationTemplateInfo import OperationTemplateInfo


class MapOperation:
    @staticmethod
    def map(operation_type):
        if operation_type == "concat":
            return OperationTemplateInfo("concat", "Соединить файлы")
        if operation_type == "split":
            return OperationTemplateInfo("split", "Разбить файлы")
        if operation_type == "rotate":
            return OperationTemplateInfo("rotate", "Повернуть страницы файлов")
        if operation_type == "archive":
            return OperationTemplateInfo("archive", "Архивировать страницы файлов")
        if operation_type == "remove_pages":
            return OperationTemplateInfo("remove_pages", "Убрать страницы из файлов")
        if operation_type == "view_doc":
            return OperationTemplateInfo("view_doc", "Просмотреть документы")
        if operation_type == "rotate_pages":
            return OperationTemplateInfo("rotate_pages", "Повернуть отдельные страницы ")
        if operation_type == "change_order":
            return OperationTemplateInfo("change_order", "Поменять порядок страниц")
