from rest_framework import serializers

from users.models import (
    UserProfile
)

from events.models import (
    Event,
    Route,
    Application,
    Result,
    AgeGroup,
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 1
        exclude = ('sponsors',)

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer
    distance = serializers.IntegerField()

    class Meta:
        model = Application
        depth = 1
        exclude = ("event", "route")

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        exclude = ("age_group",)

class AgeGroupSerializer(serializers.ModelSerializer):
    birthday_min = serializers.DateField()
    birthday_max = serializers.DateField()
    class Meta:
        model = AgeGroup
        fields = "__all__"
