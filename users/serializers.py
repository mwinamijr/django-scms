from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Accountant, CustomUser

class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isAccountant = serializers.SerializerMethodField(read_only=True)
    isTeacher = serializers.SerializerMethodField(read_only=True)
    isParent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'middle_name', 'last_name', 'isAdmin', 'isAccountant', 'isTeacher', 'isParent']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isAccountant(self, obj):
        return obj.is_accountant
    
    def get_isTeacher(self, obj):
        return obj.is_teacher
    
    def get_isParent(self, obj):
        return obj.is_parent

    def get_username(self, obj):
        name = str(obj.first_name) + str(obj.last_name)
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'middle_name', 'last_name', 'isAdmin', 'user_type', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def get_user_type(self, obj):
        serializer_data = UserSerializer(obj).data
        isAccountant = serializer_data.get('isAccountant')
        isTeacher = serializer_data.get('isTeacher')
        isParent = serializer_data.get('isParent')
        if isAccountant:
            return {'isAccountant': isAccountant}
        elif isTeacher:
            return {'isTeacher': isTeacher}
        else:
            return {'isParent': isParent}

class AccountantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accountant
        fields = "__all__"
