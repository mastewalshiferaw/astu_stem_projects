from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=100) 

    def __str__(self):
        return self.question

class ChatHistory(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chat Histories"