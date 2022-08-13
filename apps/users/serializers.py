from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
# ============================================================================ #
from apps.users.models import Customer


# =========================== USER CREATE SERIALIZER =========================== #

class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


# ============================ CUSTOMER SERIALIZER ============================ #

class CustomerSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


# ============================== USER SERIALIZER ============================== #

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']