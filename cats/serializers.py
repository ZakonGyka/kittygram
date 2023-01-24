from rest_framework import serializers
import datetime
import webcolors

from .models import Cat, Owner, Achievement, AchievementCat, CHOICES


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
    # owner = serializers.StringRelatedField(read_only=True)
    achievements = AchievementSerializer(required=False, many=True)
    age = serializers.SerializerMethodField()
    # color = serializers.ChoiceField(choices=CHOICES)
    color = Hex2NameColor()

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

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner',
                  'achievements', 'age')

    def get_age(self, obj):
        return datetime.datetime.now().year - obj.birth_year


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('id', 'first_name', 'last_name', 'cats')


