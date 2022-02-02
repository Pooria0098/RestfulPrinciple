from django.shortcuts import get_object_or_404
from rest_framework import serializers

from contacts.models import Contact, Group, CustomUser


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Contact
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'group',
            'phone_number',
            'address',
        ]

    def create(self, validated_data):
        # print('validated_data: ', validated_data)
        user = self.context.get('request').user

        first_name = validated_data.get('user').get('first_name')
        # print('first_name: ', first_name)
        last_name = validated_data.get('user').get('last_name')
        # print('last_name: ', last_name)
        email = validated_data.get('user').get('email')
        # print('email: ', email)

        group = validated_data.get('group')
        phone_number = validated_data.get('phone_number')
        address = validated_data.get('address')
        # print('group: ', group)
        # print('phone_number: ', phone_number)
        # print('address: ', address)

        created_user = CustomUser.objects.filter(id=user.id).update(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        # print('created_user: ', created_user)
        created_contact = Contact.objects.create(
            user_id=created_user,
            group=group,
            phone_number=phone_number,
            address=address
        )

        return created_contact

    def update(self, instance, validated_data):
        # print('validated_data: ', validated_data)
        # print('instance: ', instance)

        user = self.context.get('request').user

        instance.first_name = validated_data.get('user').get('first_name')
        instance.last_name = validated_data.get('user').get('last_name')
        instance.email = validated_data.get('user').get('email')

        instance.group = validated_data.get('group', instance.group)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        # print('instance.first_name: ', instance.first_name)
        # print('instance.last_name: ', instance.last_name)
        # print('instance.email: ', instance.email)
        customUser = get_object_or_404(CustomUser, id=user.id)
        customUser.first_name = instance.first_name
        customUser.last_name = instance.last_name
        customUser.email = instance.email
        customUser.save()

        Contact.objects.filter(user_id=user.id).update(
            user_id=user.id,
            group=instance.group,
            phone_number=instance.phone_number,
            address=instance.address
        )

        instance.save()
        return instance
