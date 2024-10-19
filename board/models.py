from django.db import models
from account.models import CustomUser

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='boards')
    members_num = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF',blank=True)
    def __str__(self):
        return self.name

class Member(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='board_members')  
    def __str__(self):
        return self.member.user.username
class List(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name='lists')

    def __str__(self):
        return f'{self.title} in {self.board.name}'


    
class Card(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'To-Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_members = models.ManyToManyField(Member, related_name='assigned_cards', blank=True,  null=True)
    due_date = models.DateField(blank=True, null=True)

    

