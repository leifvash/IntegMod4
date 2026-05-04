import logging, json, binascii
from json import JSONDecodeError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from .models import PaymentRecord
from .serializers import PaymentRecordSerializer

logger = logging.getLogger("django.security")

@method_decorator(ratelimit(key="ip", rate="5/m", block=False), name="create")
class PaymentRecordViewSet(viewsets.ModelViewSet):
    queryset = PaymentRecord.objects.all()
    serializer_class = PaymentRecordSerializer

    def create(self, request, *args, **kwargs):
        client_ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "unknown"))
        user_id = getattr(request.user, "id", "anon")

        #Rate limit check
        if getattr(request, "limited", False):
            logger.warning(
                "event=rate_limit_exceeded ip=%s endpoint=%s user=%s",
                client_ip, request.path, user_id
            )
            return Response({"detail": "Too Many Requests"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        try:
            if request.body:
                _ = json.loads(request.body.decode("utf-8"))
        except (JSONDecodeError, UnicodeDecodeError) as exc:
            fp = self._fingerprint(request.body)
            logger.warning(
                "event=invalid_payload ip=%s endpoint=%s user=%s fingerprint=%s error=json_decode",
                client_ip, request.path, user_id, fp
            )
            return Response({"detail": "Malformed JSON"}, status=status.HTTP_400_BAD_REQUEST)

        #Serializer validation
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            fp = self._fingerprint(request.data)
            logger.warning(
                "event=validation_failed ip=%s endpoint=%s user=%s fingerprint=%s error=%s",
                client_ip, request.path, user_id, fp, str(exc)
            )
            return Response({"detail": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

        #decryption or signature checks, catch crypto errors
        try:
            # Example placeholder: decrypt or verify here if needed
            # decrypted = decrypt_payload(request.data.get("encrypted_field"))
            pass
        except (ValueError, binascii.Error) as exc:
            fp = self._fingerprint(request.data)
            logger.warning(
                "event=invalid_encrypted_payload ip=%s endpoint=%s user=%s fingerprint=%s error=%s",
                client_ip, request.path, user_id, fp, str(exc)
            )
            return Response({"detail": "Invalid encrypted payload"}, status=status.HTTP_400_BAD_REQUEST)

        #all checks passed — proceed to create
        return super().create(request, *args, **kwargs)

    def _fingerprint(self, data):
        import hashlib, json
        try:
            s = json.dumps(data, sort_keys=True)
        except Exception:
            s = str(data)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
