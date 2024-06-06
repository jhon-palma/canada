from django.core.management.base import BaseCommand
import json
from django.db import transaction
from ..apps.properties.models import *

# This is a list of all the fields that are foreign keys; these need special handling
FK_FIELDS = [
    # ...
]

# You need to add the table names from the access database here. This is required
# if you have relations in order to add first the tables without dependencies and last
# the tables that belong on these 
TABLE_NAMES = [
    # ...
]

def fix_fks(k):
    """Add _id to the end of the field name if it is a foreign key to pass the pk of the
    foreign key instead of the whole object"""
    if k in FK_FIELDS:
        return k + '_id'
    return k

def get_model_by_table(table):
    """Get the model by the table name"""
    return getattr(models, table.capitalize())

class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):

        with open("..\\access_data.json") as f:
            j = json.load(f)

        # Delete the existing data before importing. This is optional but I find it useful
        # Notice that we delete the tables in reverse order to avoid foreign key errors
        for table in reversed(TABLE_NAMES):
            get_model_by_table(table).objects.all().delete()

        for table in TABLE_NAMES:
            for row in j[table]:
                # Create a dictionary with the column name: column value;
                # notice the fix_fks to add the _id to the column
                row_ok = {fix_fks(k): v for k,v in row.items()}
                print(row_ok)
                # Create the object; we could add thse to an array and do a bulk_create instead
                get_model_by_table(table).objects.create(**row_ok)
