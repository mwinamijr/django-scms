from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Accountant, Teacher, CustomUser

class AccountantSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Accountant
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        user = serializer.data['first_name'] + ' ' + serializer.data['last_name']
        return user

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'middle_name', 'last_name', 'isAdmin']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_username(self, obj):
        name = str(obj.first_name) + str(obj.last_name)
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)