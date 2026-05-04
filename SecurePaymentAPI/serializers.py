from rest_framework import serializers
from .models import PaymentRecord

class PaymentRecordSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True)

    class Meta:
        model = PaymentRecord
        fields = ['id', 'card_number_encrypted', 'card_number']
        read_only_fields = ['card_number_encrypted']

    def validate_card_number(self, value):
        #basic checks digits only and length between 12 and 19
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain digits only.")
        if not (12 <= len(value) <= 19):
            raise serializers.ValidationError("Card number length is invalid.")
        return value

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        record = PaymentRecord()
        record.set_card_number(card_number)
        record.save()
        return record