from flask import Response, request as flask_request
from autoscale_agent.agent import Agent
from autoscale_agent.middleware import Middleware as BaseMiddleware, RequestInfo


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with self.app.request_context(environ):
            request = flask_request
            middleware = BaseMiddleware(Agent.configuration)
            request_info = RequestInfo(request.path, request.headers)
            response = middleware.process_request(request_info)

            if isinstance(response, tuple):
                status, headers, body = response
                response = Response(body, status, headers)

            if response:
                return response(environ, start_response)

        return self.app(environ, start_response)
