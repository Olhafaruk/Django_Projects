from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]