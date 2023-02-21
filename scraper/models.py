from django.db import models

# Create your models here.
class Attraction(models.Model):
    """the locations of the attractions"""
    name = models.CharField(max_length=100, help_text="attraction name")
    description = models.TextField(blank=True, help_text="attraction description")
    location = models.CharField(max_length=100, help_text="attraction location")
    source_url = models.URLField(blank=True, help_text="attraction url")
    c_dt = models.DateTimeField(auto_now_add=False, help_text="datetime created")
    m_dt = models.DateTimeField(auto_now_add=True, help_text="datetime modified")
    is_active = models.BooleanField(help_text="usage in app")

    def __str__(self):
        return self.name
    class Meta:
        db_table = "attraction"

class MapLocation(models.Model):
    """the search results from google map"""
    search_name = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='map_result')
    name = models.CharField(max_length=100, help_text="search result name")
    description = models.TextField(blank=True, help_text="search result description")
    address = models.TextField(blank=True, help_text="location address if exists")
    gmap_id = models.CharField(max_length=100, help_text="google map id")
    source_url = models.URLField(blank=True, help_text="google map url")
    long = models.DecimalField(max_digits=9, decimal_places=6, help_text="result longitude")
    lat = models.DecimalField(max_digits=9, decimal_places=6, help_text="result latitude")
    c_dt = models.DateTimeField(auto_now_add=False, help_text="datetime created")
    m_dt = models.DateTimeField(auto_now_add=True, help_text="datetime modified")
    is_active = models.BooleanField(help_text="usage in app")

    def __str__(self):
        return self.name
    class Meta:
        db_table = "map_location"


class Review(models.Model):
    """the reviews from google map"""
    map_location = models.ForeignKey(MapLocation, on_delete=models.CASCADE, related_name='review')
    reviewer_id = models.CharField(max_length=100, help_text="reviewer id")
    reviewer_name = models.CharField(max_length=100, help_text="reviewer name")
    reviewer_level = models.CharField(max_length=10, help_text="reviewer level")
    reviewer_url = models.URLField(blank=True, help_text="reviewer url")
    reviewer_comment_count = models.IntegerField(blank=True, help_text="reviewer comment count")
    comment_id = models.CharField(max_length=100, help_text="comment id")
    comment = models.TextField(blank=True, help_text="comment text")
    comment_dt = models.DateTimeField(auto_now_add=False, help_text="comment datetime")
    is_local_guide = models.BooleanField(help_text="reviewer is a local guide or not")
    is_active = models.BooleanField(help_text="usage in app")
    c_dt = models.DateTimeField(auto_now_add=False, help_text="datetime created")
    m_dt = models.DateTimeField(auto_now_add=True, help_text="datetime modified")

    def __str__(self):
        return self.name
    class Meta:
        db_table = "review"