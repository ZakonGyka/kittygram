from rest_framework import serializers
import datetime
import webcolors
from rest_framework.validators import UniqueTogetherValidator

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES, User


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True,
                                           default=serializers.CurrentUserDefault())
    achievements = AchievementSerializer(required=False, many=True)
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOICES)
    # color = Hex2NameColor()

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner',
                  'achievements', 'age')
        read_only_fields = ('owner',)

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Cat.objects.all(),
        #         fields=('name', 'owner')
        #     )
        # ]

    def validate_birth_year(self, value):
        year = datetime.date.today().year
        if not (year - 40 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def validate(self, data):
        if data['color'] == data['name']:
            raise serializers.ValidationError(
                'Имя не может совпадать с цветом!')
        return data

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat

        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(**achievement)
            AchievementCat.objects.create(achievement=current_achievement,
                                          cat=cat)
        return cat

    def get_age(self, obj):
        return datetime.datetime.now().year - obj.birth_year


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('id', 'first_name', 'last_name', 'cats')


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'
