from social.apps.django_app.utils import strategy

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer


@strategy()
def register_by_access_token(request, backend):
    backend = request.strategy.backend
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'token':
        msg = 'No token header provided.'
        return msg

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        return msg

    access_token = auth[1]

    user = backend.do_auth(access_token)

    return user


class ObtainAuthToken(APIView):
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request, backend):
        serializer = self.serializer_class(data=request.DATA)

        if backend == 'auth':
            if serializer.is_valid():
                token, created = Token.objects.get_or_create(
                    user=serializer.object['user'])
                return Response({'token': token.key})
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = register_by_access_token(request, backend)

            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'id': user.id, 'name': user.username,
                                 'firstname': user.first_name,
                                 'userRole': 'user', 'token': token.key})


class ObtainUser(APIView):
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def get(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if request.META.get('HTTP_AUTHORIZATION'):

            auth = request.META.get('HTTP_AUTHORIZATION').split()

            if not auth or auth[0].lower() != b'token' or len(auth) != 2:
                msg = 'Invalid token header. No credentials provided.'
                return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

            token = Token.objects.get(key=auth[1])
            if token and token.user.is_active:
                return Response(
                    {'id': token.user_id, 'name': token.user.username,
                     'firstname': token.user.first_name, 'userRole': 'user',
                     'token': token.key})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)


class ObtainLogout(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def get(self, request):
        return Response({'User': ''})
