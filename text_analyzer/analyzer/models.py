from django.db import models

class ProcessedFile(models.Model):
    filename = models.CharField(max_length=255)
    processed_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(help_text="Время обработки в секундах")

    def __str__(self):
        return f"{self.filename} ({self.processing_time:.3f}s)"

