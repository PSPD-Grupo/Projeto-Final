import grpc

from auth.jwt_decoder import decode_token, InvalidTokenError
from auth.access_level import resolve_access_level, NoAccessLevelError


class _ContextWrapper(grpc.ServicerContext):
    """Encapsula o context original só pra pendurar o access_level nele,
    sem precisar mudar a assinatura dos métodos do servicer."""

    def __init__(self, context, access_level):
        self._context = context
        self.access_level = access_level

    def __getattr__(self, name):
        return getattr(self._context, name)


def _unauthenticated(message):
    def handler(request, context):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, message)
    return grpc.unary_unary_rpc_method_handler(handler)


def _permission_denied(message):
    def handler(request, context):
        context.abort(grpc.StatusCode.PERMISSION_DENIED, message)
    return grpc.unary_unary_rpc_method_handler(handler)


class JwtAuthInterceptor(grpc.ServerInterceptor):
    """Extrai o JWT do header 'authorization', valida e resolve o
    nível de acesso ANTES de qualquer RPC ser executada."""

    def __init__(self, jwt_secret: str):
        self._secret = jwt_secret

    def intercept_service(self, continuation, handler_call_details):
        token = self._extract_token(handler_call_details.invocation_metadata)

        if token is None:
            return _unauthenticated("token de autenticação ausente")

        try:
            claims = decode_token(token, self._secret)
            access_level = resolve_access_level(claims)
        except InvalidTokenError as e:
            return _unauthenticated(str(e))
        except NoAccessLevelError as e:
            return _permission_denied(str(e))

        # Segue para o método real, mas troca o context por um que carrega o nível
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