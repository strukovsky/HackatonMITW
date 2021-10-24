import json

from django.http import Http404, HttpResponseRedirect, FileResponse
from django.shortcuts import render

# Create your views here.
from main.operations.ArchiveFiles import ArchiveFiles
from main.operations.ChangePageOrderFiles import ChangePageOrderFiles
from main.operations.ClearFiles import ClearFiles
from main.operations.ConcatFiles import ConcatFiles
from main.operations.MapOperation import MapOperation
from main.operations.PreparePagesOfFiles import PreparePagesOfFiles
from main.operations.RemovePagesFiles import RemovePagesFiles
from main.operations.RotateFiles import RotateFiles
from main.operations.RotatePagesFiles import RotatePagesFiles
from main.operations.SplitFiles import SplitFiles
from main.operations.UploadFile import UploadFile


def index(request):
    return render(request, "main.html")


def prepare(request):
    operation_type = request.GET.get("type")
    if operation_type is None:
        raise Http404()
    template_info = MapOperation.map(operation_type)
    context = {
        "operation_type": operation_type,
        "operation_url": template_info.operation_url,
        "operation_text": template_info.operation_text
    }
    uploading_file = request.FILES.get("uploaded")
    files_before_upload_string = request.session.get("files")
    if files_before_upload_string is None:
        context["files"] = None
    else:
        context["files"] = json.loads(files_before_upload_string)
    if uploading_file is not None:
        current_files = UploadFile.save_PDF(uploading_file, request.session)
        request.session["files"] = json.dumps(current_files)
        context["files"] = current_files
    return render(request, "operation.html", context=context)


def concat(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    file_url = ConcatFiles.concat(files)
    context = {
        "files": [file_url]
    }
    return render(request, "result.html", context=context)


def clear(request):
    operation_type = request.GET.get("type")
    if operation_type is None:
        raise Http404()
    files_string = request.session.get("files")
    if files_string is not None:
        files = json.loads(files_string)
        ClearFiles.clear(files)
        request.session["files"] = None
    return HttpResponseRedirect("prepare?type=" + operation_type)


def storage(request):
    filename = request.GET.get("filename")
    if filename is None:
        raise Http404()
    response = FileResponse(open("storage/" + filename, 'rb'))
    return response


def split(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    resulting_filenames = SplitFiles().split(files)
    return render(request, "result.html", context={
        "files": resulting_filenames
    })


def rotate(request):
    degrees = request.GET.get("degrees")
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    if files_string is not None:
        files = json.loads(files_string)
    context = {
        "files_to_rotate": files,
    }
    if degrees is not None and files is not None:
        resulting_filenames = RotateFiles().rotate(files, degrees)
        context["rotated_files"] = resulting_filenames
    return render(request, "rotate.html", context)


def archive(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    archives = ArchiveFiles.archive(files)
    context = {
        "files": archives
    }
    return render(request, "result.html", context)


def remove_pages(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    context = {
        "files": PreparePagesOfFiles.prepare(files)
    }

    selected_file_string = request.POST.get('file')
    if selected_file_string is not None:

        selected_file = json.loads(selected_file_string.replace("\'", "\""))
        pages_count = int(selected_file['pages_count'])
        pages_to_remove = []
        for i in range(pages_count + 1):
            page_number = i + 1
            if request.POST.get(str(page_number)) is not None:
                pages_to_remove.append(i)
        result_filename = RemovePagesFiles.remove_pages(selected_file, pages_to_remove)
        return render(request, "remove_pages_result.html", {
            "filename": result_filename
        })
    return render(request, "remove_pages.html", context)


def view_doc(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    context = {
        "files": PreparePagesOfFiles.prepare(files)
    }
    return render(request, "view_doc.html", context)


def rotate_pages(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    context = {
        "files": PreparePagesOfFiles.prepare(files)
    }
    selected_file_string = request.POST.get('file')
    if selected_file_string is not None:
        selected_file = json.loads(selected_file_string.replace("\'", "\""))
        pages_count = int(selected_file['pages_count'])
        rotation = []
        for i in range(pages_count + 1):
            page_number = i + 1
            page_degrees_id = "page_" + str(page_number) + "_degrees"
            page_degrees = request.POST.get(page_degrees_id)
            if page_degrees is not None:
                rotation.append({
                    "page_number": i,
                    "degrees": int(page_degrees)
                })
        result_filename = RotatePagesFiles.rotate(selected_file, rotation)
        return render(request, "rotate_pages_result.html", {
            "filename": result_filename
        })
    return render(request, "rotate_pages.html", context)


def change_order(request):
    files_string = request.session.get("files")
    if files_string is None:
        raise Http404()
    files = json.loads(files_string)
    context = {
        "files": PreparePagesOfFiles.prepare(files)
    }
    changes = [

    ]
    for key, value in request.POST.items():
        if key.startswith('new_order_'):
            filename = key[10:]
            changes.append({
                "actual_filename": filename,
                "new_order": value
            })
    if len(changes) > 0:
        new_filenames = ChangePageOrderFiles.change(files, changes)
        return render(request, "change_order_result.html", {
            "files": new_filenames
        })
    return render(request, "change_order.html", context)


def test(request):
    return render(request, "playground.html")
