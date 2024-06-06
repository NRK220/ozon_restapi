import json
from django.core.management.base import BaseCommand
from drf.models import DeliveryMethod, Cancellation, Product, Requirement, Posting

class Command(BaseCommand):
    help = 'Load data from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The file path of the JSON file to be loaded')

    def handle(self, *args, **options):
        file_path = options['file_path']

        with open(file_path) as f:
            data = json.load(f)

        postings_data = data['result']['postings']

        for posting_data in postings_data:
            delivery_method_data = posting_data.pop('delivery_method')
            cancellation_data = posting_data.pop('cancellation')
            products_data = posting_data.pop('products')
            requirements_data = posting_data.pop('requirements')

            delivery_method, _ = DeliveryMethod.objects.get_or_create(**delivery_method_data)
            cancellation, _ = Cancellation.objects.get_or_create(**cancellation_data)
            requirements, _ = Requirement.objects.get_or_create(**requirements_data)

            posting = Posting.objects.create(
                delivery_method=delivery_method,
                cancellation=cancellation,
                requirements=requirements,
                **posting_data
            )

            product_instances = []
            for product_data in products_data:
                product, _ = Product.objects.get_or_create(**product_data)
                product_instances.append(product)
            
            posting.products.set(product_instances)
            posting.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
