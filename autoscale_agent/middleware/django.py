import os
import json
from django.http import JsonResponse, HttpResponseNotFound
from autoscale_agent.agent import Agent
from autoscale_agent.middleware import Middleware as BaseMiddleware, RequestInfo


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        middleware = BaseMiddleware(Agent.configuration, run=True)
        request_info = RequestInfo(request.path, request.META)
        response = middleware.process_request(request_info)

        if isinstance(response, tuple):
            status, headers, body = response

            if status == 200:
                response = JsonResponse(json.loads(body), safe=False)
            else:
                response = HttpResponseNotFound(body)
            for key, value in headers.items():
                response[key] = value

        if response:
            return response

        return self.get_response(request)
