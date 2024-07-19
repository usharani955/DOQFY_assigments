from django.db import models
from django.utils import timezone
import hashlib
import base64
from cryptography.fernet import Fernet

class Snippet(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    encrypted = models.BooleanField(default=False)
    secret_key_hash = models.CharField(max_length=64, blank=True, null=True)

    def set_secret_key(self, key):
        self.secret_key_hash = hashlib.sha256(key.encode()).hexdigest()

    def encrypt_content(self, key):
        fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest()))
        self.content = fernet.encrypt(self.content.encode()).decode()
        self.encrypted = True

    def decrypt_content(self, key):
        fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest()))
        return fernet.decrypt(self.content.encode()).decode()
