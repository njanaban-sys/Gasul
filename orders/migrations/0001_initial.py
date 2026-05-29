import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='cart_items', to='auth.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    to='products.product')),
            ],
            options={'unique_together': {('user', 'product')}},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(
                    choices=[('pending','Pending'),('confirmed','Confirmed'),
                             ('processing','Processing'),('shipped','Shipped'),
                             ('delivered','Delivered'),('cancelled','Cancelled')],
                    default='pending', max_length=20)),
                ('payment_method', models.CharField(
                    choices=[('cod','Cash on Delivery'),('gcash','GCash')],
                    default='cod', max_length=10)),
                ('gcash_reference', models.CharField(blank=True, default='', max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('delivery_address', models.TextField()),
                ('special_instructions', models.TextField(blank=True, default='')),
                ('admin_notes', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='orders', to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                    to='products.product')),
            ],
        ),
    ]
