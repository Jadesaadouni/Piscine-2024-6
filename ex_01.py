import pandas as pd

# Chargez les données du fichier CSV dans un DataFrame
dataset_df = pd.read_csv('dataset.csv')

print(dataset_df.columns.tolist())

def get_departements():
    onlycode_df= dataset_df.dropna(subset=['Code departement'])
    departments = onlycode_df['Code departement'].unique().astype(int)
    return {"departments": list(departments)}

#print (get_departements())

def get_towns():
    towns_data = dataset_df[['Code postal', 'Commune']].drop_duplicates()
    towns_json = towns_data.to_dict(orient='records')
    return {"towns": towns_json}

#print (get_towns())

def get_prices(department_id, town_id):
    filtered_data = dataset_df[(dataset_df['Code departement'] == department_id) & (dataset_df['Code postal'] == town_id)]
    prices_json = filtered_data[['Valeur fonciere']].to_dict(orient='records')
    return {"prices": prices_json}

#print(get_prices(44, 44690.0))

def get_prices(department_id, town_id, Rooms_min, Rooms_max):
    filtered_data = dataset_df[(dataset_df['Code departement'] == department_id) & (dataset_df['Code postal'] == town_id) & 
                         (dataset_df['Nombre pieces principales'] >= Rooms_min) & (dataset_df['Nombre pieces principales'] <= Rooms_max)]
    prices = filtered_data[['Valeur fonciere', 'Type local']].to_dict(orient='records')
    return {'prices': prices}

#print(get_prices(44, 44190.0, 0, 10))

def get_price(department_id, town_id, rooms_min=1, rooms_max=10, sq_min=20, sq_max=500):
    filtered_data = dataset_df[(dataset_df['Code departement'] == department_id) & (dataset_df['Code postal'] == town_id) &
                               (dataset_df['Nombre pieces principales'] >= rooms_min) & (dataset_df['Nombre pieces principales'] <= rooms_max)]
    if sq_min and sq_max:
        filtered_data = filtered_data[(filtered_data['Surface terrain'] >= sq_min) & (filtered_data['Surface terrain'] <= sq_max)]
    else:
        filtered_data = filtered_data[(filtered_data['Surface terrain'].isna())]

    price_json = filtered_data[['Valeur fonciere', 'Type local']].to_dict(orient='records')
    return {"prices": price_json}

#print(get_price(44, 44190.0, 1, 10, 20, 500))






