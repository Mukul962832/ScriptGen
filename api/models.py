from django.db import models

class Script(models.Model):
    title = models.CharField(max_length=255)
    prompt = models.TextField()
    script_content = models.TextField()
    language = models.CharField(max_length=50, default='English')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
