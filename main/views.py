import json

from django.http import Http404, HttpResponseRedirect, FileResponse
from django.shortcuts import render

# Create your views here.
from main.operations.ClearFiles import ClearFiles
from main.operations.ConcatFiles import ConcatFiles
from main.operations.MapOperation import MapOperation
from main.operations.SplitFile import SplitFile
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
    files = json.loads(files_string)
    resulting_filenames = SplitFile().split(files)
    return render(request, "result.html", context={
        "files": resulting_filenames
    })
