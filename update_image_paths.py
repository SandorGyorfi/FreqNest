import os
import django
import logging  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freqnest.settings')
django.setup()

from synths.models import Product

def update_image_urls():
    s3_base_url = f'https://{os.environ.get("AWS_STORAGE_BUCKET_NAME")}.s3.{os.environ.get("AWS_S3_REGION_NAME")}.amazonaws.com'

    # Debugging output
    print(f"AWS_STORAGE_BUCKET_NAME: {os.environ.get('AWS_STORAGE_BUCKET_NAME')}")
    print(f"AWS_S3_REGION_NAME: {os.environ.get('AWS_S3_REGION_NAME')}")

    for product in Product.objects.all():
        if product.image_url:
            image_name = product.image_url.split('/')[-1]  
            new_url = f'{s3_base_url}/{image_name}'
            product.image_url = new_url
            product.save()

            print(f'Updated URL for product {product.name}: {new_url}')

            logging.info(f'Updated URL for product {product.name}: {new_url}')

if __name__ == "__main__":
    update_image_urls()
