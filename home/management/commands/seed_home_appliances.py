from datetime import timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw

from home.models import Brand, Category, Color, Product, Size, Variants
from order.models import Coupon


def make_image(text, color, size=(600, 400)):
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(20, 20), (size[0] - 20, size[1] - 20)], outline='white', width=3)
    draw.text((40, size[1] // 2 - 10), text[:28], fill='white')
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f'{text.replace(" ", "_")[:30]}.jpg')


class Command(BaseCommand):
    help = 'Seed home appliances store with 20 sample products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding home appliances data...')

        brands_data = [
            'Samsung', 'Bosch', 'LG', 'Philips', 'Miele',
            'Siemens', 'Dyson', 'Whirlpool', 'KitchenAid', 'DeLonghi',
        ]
        brands = {name: Brand.objects.get_or_create(name=name)[0] for name in brands_data}

        colors = {
            name: Color.objects.get_or_create(name=name)[0]
            for name in ['White', 'Black', 'Silver', 'Stainless Steel', 'Graphite', 'Red']
        }

        trims = {
            name: Size.objects.get_or_create(name=name)[0]
            for name in ['Standard', 'Large', 'Premium']
        }

        categories = {}
        for name in ['Kitchen', 'Laundry', 'Cleaning', 'Climate Control', 'Small Appliances']:
            categories[name], _ = Category.objects.get_or_create(
                name=name,
                defaults={'sub_cat': False, 'slug': name.lower().replace(' ', '-')},
            )

        products_data = [
            {'name': 'Samsung French Door Refrigerator', 'brand': 'Samsung', 'category': ['Kitchen'], 'unit_price': 1899, 'amount': 12, 'status': 'Color', 'colors': ['Stainless Steel', 'Black'], 'color': '#1e88e5', 'tags': ['refrigerator', 'kitchen'], 'info': '<p>Energy-efficient French door refrigerator with flexible storage.</p>'},
            {'name': 'Bosch Built-in Dishwasher', 'brand': 'Bosch', 'category': ['Kitchen'], 'unit_price': 699, 'amount': 15, 'status': 'None', 'color': '#455a64', 'tags': ['dishwasher', 'kitchen'], 'info': '<p>Quiet dishwasher with multiple wash programs.</p>'},
            {'name': 'LG Front Load Washing Machine', 'brand': 'LG', 'category': ['Laundry'], 'unit_price': 899, 'amount': 10, 'status': 'Color', 'colors': ['White', 'Graphite'], 'color': '#7b1fa2', 'tags': ['washer', 'laundry'], 'info': '<p>Large-capacity washer with steam care technology.</p>'},
            {'name': 'Miele Heat Pump Dryer', 'brand': 'Miele', 'category': ['Laundry'], 'unit_price': 1099, 'amount': 8, 'status': 'None', 'color': '#c62828', 'tags': ['dryer', 'laundry'], 'info': '<p>Gentle drying with low energy consumption.</p>'},
            {'name': 'Dyson V15 Detect Vacuum', 'brand': 'Dyson', 'category': ['Cleaning'], 'unit_price': 749, 'amount': 20, 'status': 'None', 'color': '#6a1b9a', 'tags': ['vacuum', 'cleaning'], 'info': '<p>Cordless vacuum with laser dust detection.</p>'},
            {'name': 'Philips Air Fryer XXL', 'brand': 'Philips', 'category': ['Small Appliances', 'Kitchen'], 'unit_price': 349, 'amount': 25, 'status': 'None', 'color': '#ef6c00', 'tags': ['air-fryer', 'kitchen'], 'info': '<p>Healthy frying with rapid air technology.</p>'},
            {'name': 'Siemens Induction Cooktop', 'brand': 'Siemens', 'category': ['Kitchen'], 'unit_price': 1299, 'amount': 7, 'status': 'Size', 'trims': ['Standard', 'Large'], 'color': '#37474f', 'tags': ['cooktop', 'kitchen'], 'info': '<p>Precise induction cooking with touch controls.</p>'},
            {'name': 'Samsung Microwave Oven', 'brand': 'Samsung', 'category': ['Kitchen', 'Small Appliances'], 'unit_price': 299, 'amount': 30, 'status': 'None', 'color': '#0288d1', 'tags': ['microwave', 'kitchen'], 'info': '<p>Compact microwave with grill function.</p>'},
            {'name': 'Whirlpool Chest Freezer', 'brand': 'Whirlpool', 'category': ['Kitchen'], 'unit_price': 549, 'amount': 11, 'status': 'None', 'color': '#546e7a', 'tags': ['freezer', 'kitchen'], 'info': '<p>Extra storage freezer for bulk groceries.</p>'},
            {'name': 'Bosch Fully Automatic Coffee Machine', 'brand': 'Bosch', 'category': ['Small Appliances'], 'unit_price': 899, 'amount': 9, 'status': 'Color', 'colors': ['Black', 'Silver'], 'color': '#4e342e', 'tags': ['coffee', 'kitchen'], 'info': '<p>Barista-style coffee at home with one touch.</p>'},
            {'name': 'LG Dual Inverter Air Conditioner', 'brand': 'LG', 'category': ['Climate Control'], 'unit_price': 799, 'amount': 14, 'status': 'Size', 'trims': ['Standard', 'Large', 'Premium'], 'color': '#00897b', 'tags': ['ac', 'climate'], 'info': '<p>Energy-saving split AC for comfortable summers.</p>'},
            {'name': 'DeLonghi Oil Radiator Heater', 'brand': 'DeLonghi', 'category': ['Climate Control'], 'unit_price': 189, 'amount': 22, 'status': 'None', 'color': '#bf360c', 'tags': ['heater', 'climate'], 'info': '<p>Portable heater with thermostat and timer.</p>'},
            {'name': 'KitchenAid Stand Mixer', 'brand': 'KitchenAid', 'category': ['Small Appliances', 'Kitchen'], 'unit_price': 449, 'amount': 16, 'status': 'Color', 'colors': ['White', 'Red', 'Black'], 'color': '#d81b60', 'tags': ['mixer', 'baking'], 'info': '<p>Iconic stand mixer for baking enthusiasts.</p>'},
            {'name': 'Philips Hand Blender Set', 'brand': 'Philips', 'category': ['Small Appliances'], 'unit_price': 79, 'amount': 40, 'status': 'None', 'color': '#5c6bc0', 'tags': ['blender', 'kitchen'], 'info': '<p>Multi-purpose hand blender with accessories.</p>'},
            {'name': 'Samsung Jet Bot Robot Vacuum', 'brand': 'Samsung', 'category': ['Cleaning'], 'unit_price': 599, 'amount': 13, 'status': 'None', 'color': '#303f9f', 'tags': ['robot', 'vacuum'], 'info': '<p>Smart mapping robot vacuum for daily cleaning.</p>'},
            {'name': 'Bosch Built-in Electric Oven', 'brand': 'Bosch', 'category': ['Kitchen'], 'unit_price': 999, 'amount': 6, 'status': 'Size', 'trims': ['Standard', 'Premium'], 'color': '#263238', 'tags': ['oven', 'kitchen'], 'info': '<p>Even baking with pyrolytic self-cleaning option.</p>'},
            {'name': 'Philips Smart LED Lamp Pack', 'brand': 'Philips', 'category': ['Climate Control'], 'unit_price': 129, 'amount': 35, 'status': 'None', 'color': '#fdd835', 'tags': ['lighting', 'smart-home'], 'info': '<p>Wi-Fi enabled bulbs with app control.</p>'},
            {'name': 'Miele Washer Dryer Combo', 'brand': 'Miele', 'category': ['Laundry'], 'unit_price': 1599, 'amount': 5, 'status': 'Color', 'colors': ['White', 'Graphite'], 'color': '#880e4f', 'tags': ['combo', 'laundry'], 'info': '<p>All-in-one wash and dry for compact homes.</p>'},
            {'name': 'Siemens Chimney Hood', 'brand': 'Siemens', 'category': ['Kitchen'], 'unit_price': 459, 'amount': 18, 'status': 'None', 'color': '#607d8b', 'tags': ['hood', 'kitchen'], 'info': '<p>Powerful extraction with low noise levels.</p>'},
            {'name': 'LG PuriCare Tower Fan', 'brand': 'LG', 'category': ['Climate Control'], 'unit_price': 399, 'amount': 17, 'status': 'Color', 'colors': ['White', 'Silver'], 'color': '#00acc1', 'tags': ['fan', 'air-purifier'], 'info': '<p>Tower fan with air purification filter.</p>'},
        ]

        created_count = 0
        for data in products_data:
            slug = data['name'].lower().replace(' ', '-').replace("'", '')
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'brand': brands[data['brand']],
                    'unit_price': data['unit_price'],
                    'amount': data['amount'],
                    'status': data['status'],
                    'information': data['info'],
                    'available': True,
                },
            )
            if created:
                created_count += 1
                product.image.save(slug + '.jpg', make_image(data['name'], data['color']), save=True)
                for cat_name in data['category']:
                    product.category.add(categories[cat_name])
                for tag in data.get('tags', []):
                    product.tags.add(tag)
                for color_name in data.get('colors', []):
                    product.color.add(colors[color_name])
                for trim_name in data.get('trims', []):
                    product.size.add(trims[trim_name])

                if data['status'] == 'Color':
                    for color_name in data.get('colors', []):
                        Variants.objects.create(
                            name=f'{data["name"]} - {color_name}',
                            product_variant=product,
                            color_variant=colors[color_name],
                            unit_price=data['unit_price'],
                            amount=max(2, data['amount'] // 3),
                        )
                elif data['status'] == 'Size':
                    for i, trim_name in enumerate(data.get('trims', [])):
                        Variants.objects.create(
                            name=f'{data["name"]} - {trim_name}',
                            product_variant=product,
                            size_variant=trims[trim_name],
                            unit_price=data['unit_price'] + (i * 100),
                            amount=max(2, data['amount'] // 3),
                        )

        now = timezone.now()
        Coupon.objects.get_or_create(
            code='HOME10',
            defaults={'active': True, 'start': now - timedelta(days=1), 'end': now + timedelta(days=90), 'discount': 10},
        )
        Coupon.objects.get_or_create(
            code='WELCOME15',
            defaults={'active': True, 'start': now - timedelta(days=1), 'end': now + timedelta(days=30), 'discount': 15},
        )

        self.stdout.write(self.style.SUCCESS(
            f'Home appliances store seeded: {created_count} new products, {Product.objects.count()} total.'
        ))
