from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='site_name',
            field=models.CharField(default='Simulador CS', max_length=100, verbose_name='Nombre del Sitio'),
        ),
    ]
