from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "role"]

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create(
            username = validated_data['username'],
            role = validated_data['role'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data