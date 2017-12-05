# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-01 06:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokemon_app', '0006_auto_20171130_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryTrios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_child', to='pokemon_app.Pokemon')),
                ('child_egg_move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_child_egg_move', to='pokemon_app.Moves')),
                ('parent1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_1', to='pokemon_app.Pokemon')),
                ('parent2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_2', to='pokemon_app.Pokemon')),
                ('parent_level_up_move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historytrios_parent_level_up_move', to='pokemon_app.Moves')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]