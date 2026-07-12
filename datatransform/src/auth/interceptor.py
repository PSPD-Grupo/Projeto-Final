import grpc

from auth.jwt_decoder import decode_token, TokenExpiredError, TokenMalformedError
from auth.access_level import resolve_access_level, NoAccessLevelError

class _ContextWrapper:
    def __init__(self, context, access_level):
        self._context = context
        self.access_level = access_level

    def __getattr__(self, name):
        return getattr(self._context, name)


def _abort_handler(code, message, reason):
    def handler(request, context):
        context.set_trailing_metadata((("error-reason", reason),))
        context.abort(code, message)
    return grpc.unary_unary_rpc_method_handler(handler)


class JwtAuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, jwt_secret: str):
        self._secret = jwt_secret

    def intercept_service(self, continuation, handler_call_details):
        token = self._extract_token(handler_call_details.invocation_metadata)

        if token is None:
            return _abort_handler(
                grpc.StatusCode.UNAUTHENTICATED,
                "token de autenticação ausente",
                "TOKEN_MISSING",
            )

        try:
            claims = decode_token(token, self._secret)
            access_level = resolve_access_level(claims)
        except TokenExpiredError as e:
            return _abort_handler(grpc.StatusCode.UNAUTHENTICATED, str(e), "TOKEN_EXPIRED")
        except TokenMalformedError as e:
            return _abort_handler(grpc.StatusCode.UNAUTHENTICATED, str(e), "TOKEN_INVALID")
        except NoAccessLevelError as e:
            return _abort_handler(grpc.StatusCode.PERMISSION_DENIED, str(e), "NO_ACCESS_LEVEL")

        handler = continuation(handler_call_details)
        return self._wrap_handler(handler, access_level)

    @staticmethod
    def _extract_token(metadata):
        for key, value in metadata or []:
            if key.lower() == "authorization" and value.startswith("Bearer "):
                return value[len("Bearer "):]
        return None

    @staticmethod
    def _wrap_handler(handler, access_level):
        if handler is None or not handler.unary_unary:
            return handler

        original = handler.unary_unary

        def wrapped(request, context):
            return original(request, _ContextWrapper(context, access_level))

        return grpc.unary_unary_rpc_method_handler(
            wrapped,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )