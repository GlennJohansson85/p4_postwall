import os
import env  # Ensure this is importing your env.py correctly

# Access and print environment variables
print("AWS_ACCESS_KEY_ID:", os.environ['AWS_ACCESS_KEY_ID'])
print("AWS_SECRET_ACCESS_KEY:", os.environ['AWS_SECRET_ACCESS_KEY'])
print("AWS_STORAGE_BUCKET_NAME:", os.environ['AWS_STORAGE_BUCKET_NAME'])
print("AWS_S3_REGION_NAME:", os.environ['AWS_S3_REGION_NAME'])
print("SECRET_KEY:", os.environ['SECRET_KEY'])