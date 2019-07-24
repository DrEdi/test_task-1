from celery_config.celery import app
from core.models import Post
from datetime import datetime


@app.task(name="update-posts")
def update_posts():
    Post.objects.all().update(title=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
