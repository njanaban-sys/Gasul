from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Feedback


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...\n')

        # ── Categories ────────────────────────────────────────────
        cats_data = [
            {'name': 'LPG Cylinders',   'slug': 'lpg',         'icon': '🔥', 'order': 1,
             'description': 'Standard and industrial LPG gas cylinders'},
            {'name': 'Refill Services', 'slug': 'refill',      'icon': '♻️', 'order': 2,
             'description': 'Cylinder refill services for all sizes'},
            {'name': 'Accessories',     'slug': 'accessories', 'icon': '🔧', 'order': 3,
             'description': 'Regulators, hoses, stoves, and safety accessories'},
        ]
        cat_map = {}
        for c in cats_data:
            obj, created = Category.objects.get_or_create(slug=c['slug'], defaults=c)
            cat_map[c['slug']] = obj
            self.stdout.write(f'  {"✅" if created else "⏭ "} category: {obj.name}')

        # ── Products ──────────────────────────────────────────────
        products_data = [
            # LPG
            {'name': 'GASUL 11kg LPG Cylinder',
             'description': 'Standard household 11kg LPG cylinder. Safe and long-lasting.',
             'price': 680.00, 'stock': 50, 'cat': 'lpg',         'discount_percent': 0},
            {'name': 'GASUL 22kg LPG Cylinder',
             'description': 'Heavy-duty 22kg LPG cylinder for high-usage households.',
             'price': 1250.00, 'stock': 30, 'cat': 'lpg',        'discount_percent': 5},
            {'name': 'GASUL 50kg Industrial LPG',
             'description': 'Large 50kg industrial LPG tank for commercial use.',
             'price': 2800.00, 'stock': 10, 'cat': 'lpg',        'discount_percent': 0},
            {'name': 'GASUL 2.7kg Portable LPG',
             'description': 'Compact portable cylinder for camping and outdoor cooking.',
             'price': 320.00, 'stock': 75, 'cat': 'lpg',         'discount_percent': 10},
            # Refill
            {'name': '11kg Cylinder Refill',
             'description': 'Refill service for standard 11kg cylinders.',
             'price': 480.00, 'stock': 999, 'cat': 'refill',     'discount_percent': 0},
            {'name': '22kg Cylinder Refill',
             'description': 'Refill service for 22kg LPG cylinders.',
             'price': 900.00, 'stock': 999, 'cat': 'refill',     'discount_percent': 0},
            {'name': '50kg Industrial Refill',
             'description': 'Industrial tank refill. Prior scheduling required.',
             'price': 2100.00, 'stock': 200, 'cat': 'refill',    'discount_percent': 0},
            {'name': '2.7kg Portable Refill',
             'description': 'Quick refill for portable camping cylinders.',
             'price': 230.00, 'stock': 500, 'cat': 'refill',     'discount_percent': 5},
            # Accessories
            {'name': 'High-Pressure LPG Regulator',
             'description': 'Durable regulator with safety pressure gauge.',
             'price': 350.00, 'stock': 40, 'cat': 'accessories', 'discount_percent': 0},
            {'name': 'Standard LPG Hose (1.5m)',
             'description': '1.5-meter reinforced rubber LPG hose. Safety-tested.',
             'price': 120.00, 'stock': 100, 'cat': 'accessories', 'discount_percent': 0},
            {'name': 'Double-Burner Gas Stove',
             'description': 'Stainless steel double-burner stove. Easy to clean.',
             'price': 1450.00, 'stock': 20, 'cat': 'accessories', 'discount_percent': 15},
            {'name': 'LPG Leak Detector',
             'description': 'Electronic leak detector with audible alarm.',
             'price': 280.00, 'stock': 35, 'cat': 'accessories', 'discount_percent': 0},
            {'name': 'Cylinder Safety Cap',
             'description': 'Protective cap for LPG cylinder valves.',
             'price': 45.00, 'stock': 200, 'cat': 'accessories', 'discount_percent': 0},
            {'name': 'Gas Stove Knob Set (4pcs)',
             'description': 'Replacement knob set for standard gas stoves.',
             'price': 85.00, 'stock': 60, 'cat': 'accessories',  'discount_percent': 0},
        ]
        for p in products_data:
            cat = cat_map[p.pop('cat')]
            obj, created = Product.objects.get_or_create(
                name=p['name'], defaults={**p, 'category': cat}
            )
            self.stdout.write(f'  {"✅" if created else "⏭ "} product: {obj.name}')

        # ── Users ─────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@gasul.ph', 'admin123')
            self.stdout.write('  ✅ superuser: admin / admin123')
        else:
            self.stdout.write('  ⏭  superuser: admin')

        if not User.objects.filter(username='customer1').exists():
            User.objects.create_user('customer1', 'customer1@example.com', 'customer123')
            self.stdout.write('  ✅ user: customer1 / customer123')
        else:
            self.stdout.write('  ⏭  user: customer1')

        # ── Sample feedback ───────────────────────────────────────
        for fb in [
            {'name': 'Maria Santos',   'rating': 5,
             'message': 'Super fast delivery! Very happy with GASUL LPG!'},
            {'name': 'Juan dela Cruz', 'rating': 4,
             'message': 'Good service. The regulator I bought is working great.'},
            {'name': 'Ana Reyes',      'rating': 5,
             'message': 'Love the GCash payment option! Very convenient.'},
        ]:
            if not Feedback.objects.filter(name=fb['name']).exists():
                Feedback.objects.create(**fb, is_published=True)
                self.stdout.write(f'  ✅ feedback: {fb["name"]}')

        self.stdout.write('\n🎉 Done!\n')
        self.stdout.write('  Admin login:    admin / admin123')
        self.stdout.write('  Customer login: customer1 / customer123')
        self.stdout.write('  Run:            python manage.py runserver')
