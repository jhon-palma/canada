import json

def get_ctype(t):
    """Depending on the type of each column add a different field in the model"""
    if t == "str":
        return "TextField(blank=True, )"
    elif t == "int":
        return "IntegerField(blank=True, null=True)"
    elif t == "float":
        return "FloatField(blank=True, null=True)"
    elif t == "bool":
        return "BooleanField(blank=True, null=True)"
    elif t == "datetime":
        return "DateTimeField(blank=True, null=True)"
    elif t == "date":
        return "DateField(blank=True, null=True)"
    elif t == "Decimal":
        return "DecimalField(blank=True, null=True, max_digits=15, decimal_places=5)"
    else:
        print(t)
        raise NotImplementedError

# Load the descriptions we created in the previous step
descriptions = json.load(open("..\\access_description.json"))

# mlines will be an array of the lines of the models.py file
mlines = ["from django.db import models", "", ""]

for d in descriptions:
    # Create a model for each table
    mname = d["fixed_table_name"].capitalize()
    mlines.append(f"class {mname}(models.Model):")
    for c in d["columns"]:
        ctype = get_ctype(c["type"])
        mlines.append(f"    {c['fixed_name']} = models.{ctype}")
    mlines.append("")
    mlines.append("    class Meta:")
    mlines.append(f"        db_table = '{d['fixed_table_name']}'")
    mlines.append(f"        verbose_name = '{d['table_name']}'")

    mlines.append("")
    mlines.append("")


with open("..\\access_models.py", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(mlines))