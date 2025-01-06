from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from api.serializers import *
  

class EventDetailAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.filter(active=True).order_by('pk')
    serializer_class = EventSerializer


class EventListAPIView(ListAPIView, EventDetailAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.filter(active=True, finished=False).order_by('date')


class ApplicationListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):        
        return Application.objects.filter(event__pk=self.kwargs['event__pk'])

  
class ResultListCreateUpdateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer
    model = Result

    def get_queryset(self):        
        return Result.objects.filter(event__pk=self.kwargs['event__pk']).order_by('route')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)


        for item in request.data:
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)

            instance = self.model.objects.filter(
                event_id = item.get('event'),
                route_id = item.get('route'),
                user_profile_id = item.get('user_profile')
                ).first()
            
            if instance:
                serializer.update(instance, serializer.validated_data)
            else:
                instance = serializer.save()
                instance:Result
                
                application = Application.objects.filter(
                    event = instance.event,
                    route = instance.route,
                    user_profile = instance.user_profile,
                ).first()

                if application:
                    application.result = instance
                    application.save()

                    instance.age_group = application.agegroup()
                    instance.save()


        return Response(status=status.HTTP_202_ACCEPTED)

