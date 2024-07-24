from django.db import migrations

def delete_recommandations(apps, schema_editor):
    Recommandation = apps.get_model('marketingSystemApp', 'Recommandation')
    Recommandation.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('marketingSystemApp', '0011_rename_rating_financingrequest_content'),
    ]

    operations = [
        migrations.RunPython(delete_recommandations),
    ]
