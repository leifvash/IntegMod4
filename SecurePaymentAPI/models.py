from django.db import models
from .encryption_utils import encrypt_data, decrypt_data

class PaymentRecord(models.Model):
    card_number_encrypted = models.TextField()

    def set_card_number(self, card_number: str):
        self.card_number_encrypted = encrypt_data(card_number)

    def get_card_number(self) -> str:
        return decrypt_data(self.card_number_encrypted)
