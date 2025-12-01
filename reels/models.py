import uuid
from django.db import models
from django.utils import timezone


class ReelJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('script_pending_approval', 'script_pending_approval'),  # Waiting for user to approve script
        ('script_approved', 'script_approved'),  # Script approved, ready for processing
        ('processing', 'processing'),  # Generating audio/video
        ('done', 'done'),
        ('error', 'error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    original_script = models.TextField()
    final_script = models.TextField(blank=True, null=True)  # Approved script (after user approval)
    tone = models.CharField(max_length=50, default='neutral')
    script_approved = models.BooleanField(default=False)  # Whether user approved the script
    
    image = models.ImageField(upload_to='reels/images/')
    audio_file = models.FileField(upload_to='reels/audio/', null=True, blank=True)
    video_file = models.FileField(upload_to='reels/video/', null=True, blank=True)
    
    status = models.CharField(
        max_length=25,  # Increased to accommodate 'script_pending_approval' (23 chars)
        choices=STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"ReelJob {self.id} - {self.status}"

