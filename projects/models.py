from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Web', 'Web Development'),
        ('Mobile', 'Mobile App'),
        ('System', 'System Software'),
        ('AI/ML', 'AI & Machine Learning'),
        ('Cloud', 'Cloud Solutions'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500, help_text="Comma separated technologies")
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    live_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', null=True, blank=True)
    email = models.EmailField(blank=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma separated skills")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name