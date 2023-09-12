import json
from mongoengine import connect, Document, StringField, IntField, FloatField

# Se connecter à la base de données MongoDB
connect('pool-day6', host='localhost', port=27017)

# Définir le modèle de données
class RealEstate(Document):
    month = StringField(required=True)
    region = StringField(required=True)
    department = StringField(required=True)
    type = StringField(required=True)
    sales = IntField(required=True)
    rooms = FloatField(required=True)
    garden_sqm = FloatField()
    value = FloatField(required=True)

# Charger les données à partir du JSON (remplacez le chemin par le vôtre)
with open('maisons_appartements_data.json', 'r') as json_file:
    data = json.load(json_file)
    for entry in data:
        real_estate_entry = RealEstate(
            month=entry['month'],
            region=entry['region'],
            department=entry['department'],
            type=entry['type'],
            sales=entry['sales'],
            rooms=entry['rooms'],
            garden_sqm=entry.get('garden_sqm', None),
            value=entry['value']
        )
        real_estate_entry.save()

# Calculer les statistiques demandées
# - Le nombre de ventes global
total_sales_global = RealEstate.objects().sum('sales')
# - Le nombre moyen de pièces global
average_rooms_global = RealEstate.objects().average('rooms')
# - Le ratio appartements/maisons global
apartment_ratio_global = (RealEstate.objects(type='apartment').sum('sales') / RealEstate.objects(type='house').sum('sales')).round(2)
# - La surface moyenne des jardins des maisons global
average_garden_sqm_global = RealEstate.objects(type='house', garden_sqm__gt=0).average('garden_sqm')
# - La valeur moyenne des maisons avec et sans jardin global
average_house_value_with_garden_global = RealEstate.objects(type='house', garden_sqm__gt=0).average('value')
average_house_value_without_garden_global = RealEstate.objects(type='house', garden_sqm=0).average('value')
# - La valeur moyenne des logements en fonction du nombre de pièces global
average_value_by_rooms_global = RealEstate.objects().group_by('rooms', {'value': 'avg'})

# Afficher les statistiques globales
print("Statistiques globales :")
print(f"Nombre total de ventes global : {total_sales_global}")
print(f"Nombre moyen de pièces global : {average_rooms_global}")
print(f"Ratio global appartements/maisons : {apartment_ratio_global}")
print(f"Surface moyenne des jardins des maisons global : {average_garden_sqm_global}")
print(f"Valeur moyenne des maisons avec jardin global : {average_house_value_with_garden_global}")
print(f"Valeur moyenne des maisons sans jardin global : {average_house_value_without_garden_global}")
print("Valeur moyenne des logements en fonction du nombre de pièces global :")
for item in average_value_by_rooms_global:
    print(f"  {item['rooms']} pièces : {item['value']}")