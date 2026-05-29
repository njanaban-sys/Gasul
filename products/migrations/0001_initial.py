from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('icon', models.CharField(default='🔥', max_length=10)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, default='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10,
                    validators=[django.core.validators.MinValueValidator(0)])),
                ('stock', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                    related_name='products', to='products.category')),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5,
                    validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='wishlist', to='auth.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    to='products.product')),
            ],
            options={'unique_together': {('user', 'product')}},
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, default='')),
                ('rating', models.PositiveSmallIntegerField(
                    choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], default=5)),
                ('message', models.TextField()),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
