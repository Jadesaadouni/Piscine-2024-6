from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

#Charger le fichier CSV
dataset_df = pd.read_csv('dataset.csv')

@app.route('/departments', methods=['GET'])
def get_departments():
    without_nan = dataset_df.dropna(subset=['Code departement'])
    departments = without_nan['Code departement'].unique().astype(int)
    return jsonify({"departments": list(departments)})

@app.route('/towns', methods=['GET'])
def get_towns():
    towns_data = dataset_df[['Code postal', 'Commune']].drop_duplicates()
    towns_json = towns_data.to_dict(orient='records')
    return jsonify({"towns": towns_json})

@app.route('/prices/departments/<int:department_id>', methods=['GET'])
def get_prices(department_id):
    room_min = request.args.get('room_min', type=int)
    room_max = request.args.get('room_max', type=int)
    sq_min = request.args.get('sq_min', type=int)
    sq_max = request.args.get('sq_max', type=int)

    filtered_data = dataset_df[dataset_df['Code departement'] == department_id]

    if room_min is not None and room_max is not None:
        filtered_data = filtered_data[(filtered_data['Nombre pieces principales'] >= room_min) & (filtered_data['Nombre pieces principales'] <= room_max)]

    if sq_min is not None and sq_max is not None:
        filtered_data = filtered_data[(filtered_data['Surface terrain'] >= sq_min) & (filtered_data['Surface terrain'] <= sq_max)]
    else:
        filtered_data = filtered_data[filtered_data['Surface terrain'].isna()]

    prices_json = filtered_data[['Valeur fonciere', 'Type local']].to_dict(orient='records')
    return jsonify({"prices": prices_json})
@app.route('/prices/departments/<int:department_id>/towns/<float:town_id>', methods=['GET'])
def get_prices_by_town(department_id, town_id):
    room_min = request.args.get('room_min', type=int)
    room_max = request.args.get('room_max', type=int)
    sq_min = request.args.get('sq_min', type=int)
    sq_max = request.args.get('sq_max', type=int)

    filtered_data = dataset_df[(dataset_df['Code departement'] == department_id) & (dataset_df['Code postal'] == town_id)]

    if room_min is not None and room_max is not None:
        filtered_data = filtered_data[(filtered_data['Nombre pieces principales'] >= room_min) & (filtered_data['Nombre pieces principales'] <= room_max)]

    if sq_min is not None and sq_max is not None:
        filtered_data = filtered_data[(filtered_data['Surface terrain'] >= sq_min) & (filtered_data['Surface terrain'] <= sq_max)]
    else:
        filtered_data = filtered_data[filtered_data['Surface terrain'].isna()]

    prices_json = filtered_data[['Valeur fonciere', 'Type local']].to_dict(orient='records')
    return jsonify({"prices": prices_json})

if __name__ == '__main__':
    app.run(debug=True)