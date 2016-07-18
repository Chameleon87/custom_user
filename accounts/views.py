from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from django.views.decorators.csrf import csrf_exempt

from serializers import AcUserSerializer, AuthCustomTokenSerializer
from models import AcUser


# Create your views here.

class RegisterView(CreateAPIView):
    """
    Register View
    """
    queryset = AcUser.objects.all()
    serializer_class = AcUserSerializer

@csrf_exempt
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthCustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_type, created = AcUser.objects.get_or_create(user_type=user_type)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_type': user.user_type})
