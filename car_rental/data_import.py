import os
import sys
import pandas as pd
import re
from django.db.models import Count

# Set the DJANGO_SETTINGS_MODULE environment variable manually
os.environ['DJANGO_SETTINGS_MODULE'] = 'car_rental.settings'  # Replace with your project settings

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import Django setup and models
import django

django.setup()

from app.models import Car  # Replace 'app' with your app name

# Path to your CSV file
file_path = r'D:\car_data.csv'  # Update this path to your CSV file


def clean_decimal(value):
    """Clean and convert string to decimal, handling non-numeric text."""
    if isinstance(value, str):
        # Extract digits (including decimal points) from the string
        value = re.sub(r'[^\d.,]', '', value)  # Remove any non-numeric characters except digits and commas

        # If the value is not empty after cleaning, replace commas and convert to float
        return float(value.replace(',', '')) if value else None
    elif isinstance(value, (int, float)):  # If it's already a number, return it as a float
        return float(value)
    return None  # Return None if the value is neither string nor number


def process_csv(file_path):
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Iterate over each row of the DataFrame and insert data into the model
    for _, row in df.iterrows():
        Car.objects.create(
            brand=row['Brand'],
            model=row['Model'],
            rent_per_hour=clean_decimal(row['Rent Per Hour']),
            buying_price=clean_decimal(row['Buying Price (INR)']),
            engine_specs=row['Engine Specs'],
            mileage=clean_decimal(row['Mileage (km/l)']),
            transmission=row['Transmission'],
            fuel_type=row['Fuel Type'],
            seating_capacity=int(row['Seating Capacity']),  # Convert to integer
            image_url=row['Image URL'],
        )
    print("Data uploaded successfully!")

def remove_duplicates():

    duplicate_cars = (
        Car.objects.values('brand', 'model')
        .annotate(car_count=Count('id'))
        .filter(car_count__gt=1)
    )

    # Iterate over duplicate groups and remove duplicates
    for duplicate in duplicate_cars:
        brand = duplicate['brand']
        model = duplicate['model']

        # Fetch all cars with the same brand and model
        cars_to_delete = Car.objects.filter(brand=brand, model=model)

        # Keep the first car and delete the rest
        cars_to_delete.exclude(id=cars_to_delete.first().id).delete()

    print("Duplicate data removed successfully!")


# Call the function to process the file and upload the data
process_csv(file_path)
remove_duplicates()