import os
import re
from mimetypes import MimeTypes

from django.conf import settings
from django.http import FileResponse, HttpResponse

mime = MimeTypes()


def static_file(request):
    """
    static/으로 시작하는 모든 URL이 이 뷰에 매칭되어야 함
        -> urls.py에 해당 정규표현식과 이 뷰를 매칭

    request.path에서
        /static/<FILE_PATH>/
    path변수에 FILE_PATH에 해당하는 문자열을 변수로 할당

    os.path모듈을 사용해 settings.BASE_DIR로부터
    현재 프로젝트 구조의 static폴더내부에서 path에 해당하는 파일이 있는지 검사
    있으면 해당 파일을 리턴, 없으면 HttpResponse(status=404)를 리턴

    파일을 리턴할때에는
        https://docs.djangoproject.com/en/1.11/ref/request-response/#fileresponse-objects

    이미지 등 파일을 리턴할때에는 Response에 content_type을 설정
        https://stackoverflow.com/questions/14412211/get-mimetype-of-file-python

    :param request:
    :return:
    """
    path = re.search(r'^/static/(.*)', request.path).group(1)
    paths = path.split('/')
    paths.insert(0, 'static')

    base_dir = settings.BASE_DIR
    file_path = os.path.join(base_dir, *paths)
    mime_type = mime.guess_type(file_path)

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, 'rb'),
            content_type=mime_type)
    return HttpResponse('File not found', status=404)
