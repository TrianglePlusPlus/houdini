import json

from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        super(JsonResponse, self).__init__(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')),
            content_type='application/json', *args, **kwargs)
