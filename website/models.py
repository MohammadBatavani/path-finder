from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from django.contrib.auth.models import User

# Create your models here.

def map_dir_path(instance, filename):
    return 'Map/{0}/{1}'.format(instance.name, filename)

class Map(models.Model):
    name = models.CharField(max_length=64)
    height_map = models.ImageField(upload_to=map_dir_path)
    forbidden_map = models.ImageField(upload_to=map_dir_path)
    visual_map = models.ImageField(upload_to=map_dir_path)
    width_meter = models.IntegerField()

    def __str__(self):
        return self.name

class Map_Thread(models.Model):
    thread_address = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    working_map = models.ForeignKey(Map, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    algorithm = models.CharField(max_length=64)

    def __str__(self):
        return self.thread_address

class History(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_history')
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    start_point = models.JSONField()
    destination_point = models.JSONField()
    res_dir = models.JSONField()
    res_dir_distance = models.FloatField()
    res_2d_distance = models.FloatField()
    res_time_of_arrival = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.map

class Algorithm(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=Map)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for file in [instance.height_map, instance.forbidden_map, instance.visual_map]:
        if file:
            if os.path.isfile(file.path):
                os.remove(file.path)

@receiver(pre_save, sender=Map)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    for old_file, new_file in {Map.objects.get(pk=instance.pk).height_map: instance.height_map,
                               Map.objects.get(pk=instance.pk).forbidden_map: instance.forbidden_map,
                               Map.objects.get(pk=instance.pk).visual_map: instance.visual_map, }.items():
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

@receiver(post_delete, sender=Map_Thread)
def auto_finish_thread_on_delete(sender, instance, **kwargs):
    from core.A_Star import A_Star
    core_algorithm = {
        'A_Star': A_Star
    }
    core_algorithm.get(instance.algorithm).kill_instance(instance.thread_address)
    core_algorithm.get(instance.algorithm).update_instances()