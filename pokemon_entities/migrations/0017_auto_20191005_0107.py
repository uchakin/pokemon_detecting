# Generated by Django 2.2.3 on 2019-10-04 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0016_auto_20191005_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evolution', to='pokemon_entities.Pokemon'),
        ),
    ]
