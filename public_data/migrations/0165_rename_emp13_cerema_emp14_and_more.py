# Generated by Django 4.2.11 on 2024-05-02 13:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("public_data", "0164_remove_cerema_libaav2020"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cerema",
            old_name="emp13",
            new_name="emp14",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="emp1319",
            new_name="emp1420",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="emp19",
            new_name="emp20",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="men13",
            new_name="men14",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="men1319",
            new_name="men1420",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="men19",
            new_name="men20",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="pop13",
            new_name="pop14",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="pop1319",
            new_name="pop1420",
        ),
        migrations.RenameField(
            model_name="cerema",
            old_name="pop19",
            new_name="pop20",
        ),
    ]
