from flask import Flask, jsonify, render_template, request
import pandas as pd
import os, re

# configuration
DEBUG = True
dir_path = "static/tis/"

# Initialize
app = Flask(__name__)
app.debug = True

#Build List with all vehicles
files = os.listdir("./static/tis")
rows_list = []
for i in range(0, len(files)):
    fn_split = files[i].split('_')
    dict1 = {}
    dict1["model"] = (fn_split[0] + " " + fn_split[2])
    dict1["motor"] = fn_split[3] + " (" + fn_split[4] + ")"
    dict1["country"] = fn_split[1]
    dict1["handdrive"] = fn_split[5]
    dict1["year"] = re.split('(\d+)', fn_split[6].split('.')[0])[0] + " " + re.split('(\d+)', fn_split[6].split('.')[0])[1]
    rows_list.append(dict1)
cars = pd.DataFrame(rows_list)

def create_options(inputlist):
    new_list = []
    for el in inputlist:
        new_list.append('<option value="'+el+'">'+el+'</option>')
    new_list.sort()
    new_list.insert(0, '<option value="#">Bitte Auswählen</option>')
    return new_list

def filter_for_car(car, cat, subcat):
    filename = (car["model"].split(" ")[0])+"_"+car["country"]+"_"+(car["model"].split(" ")[1])+"_"+car["engine"].replace(" ", "_").replace("(", "").replace(")", "")+"_"+car["hd"]+"_"+car["year"].replace(" ", "")+".csv"
    df = pd.read_csv(dir_path+filename)
    df = df[df.category.str.match(cat) | df.subcategory.str.match(subcat)]
    return df

@app.route('/')
def select_model():
    models = cars.model.unique()
    model_list = []
    for model in models:
        model_list.append(model)
    model_list.sort()
    return render_template('index.html', title='Car Selection', model_list = model_list)

@app.route('/select_model', methods=['POST'])
def select_engine():
    selected_model = request.form['selected_model']
    engines = cars[cars.model == selected_model].motor.unique()
    engine_list = create_options(engines)
    return jsonify(engine_list)

@app.route('/select_engine', methods=['POST'])
def select_country():
    selected_model = request.form['selected_model']
    selected_engine = request.form['selected_engine']
    countries = cars[(cars.model == selected_model) & (cars.motor == selected_engine)].country.unique()
    country_list = create_options(countries)
    return jsonify(country_list)

@app.route('/select_country', methods=['POST'])
def select_hd():
    selected_model = request.form['selected_model']
    selected_engine = request.form['selected_engine']
    selected_country = request.form['selected_country']
    hds = cars[(cars.model == selected_model) & (cars.motor == selected_engine) & (cars.country == selected_country)].handdrive.unique()
    hd_list = create_options(hds)
    return jsonify(hd_list)

@app.route('/select_hd', methods=['POST'])
def select_year():
    selected_model = request.form['selected_model']
    selected_engine = request.form['selected_engine']
    selected_country = request.form['selected_country']
    selected_hd = request.form['selected_hd']
    years = cars[(cars.model == selected_model) & (cars.motor == selected_engine) & (cars.country == selected_country) & (cars.handdrive == selected_hd)].year.unique()
    year_list = create_options(years)
    return jsonify(year_list)

@app.route('/select_categories', methods=['POST'])
def select_categories():
    car = {
        "model" : request.form.get('selected_model'),
        "engine": request.form.get('selected_engine'),
        "country": request.form.get('selected_country'),
        "hd": request.form.get('selected_hd'),
        "year": request.form.get('selected_year')
    }
    df_c2 = filter_for_car(car, "", "")
    cats = df_c2.category.unique()
    cats.sort()
    possible_cats = []
    for el in cats:
        possible_cats.append('<input type="checkbox" class="option" name="'+el+'"><label for="'+el+'">'+el+'</label>')
        subcats = df_c2[df_c2.category == el].subcategory.unique()
        if len(subcats) > 0:
            subcats.sort()
            possible_cats.append('<ul>')
            for sl in subcats:
                possible_cats.append('<li><label><input type="checkbox" class="subOption" name="'+sl+'">'+sl+'</label></li>')
            possible_cats.append('</ul><br/>')
    return jsonify(possible_cats)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    car1 = {
        "model" : request.form.get('selected_model'),
        "engine": request.form.get('selected_engine'),
        "country": request.form.get('selected_country'),
        "hd": request.form.get('selected_hd'),
        "year": request.form.get('selected_year')
    }
    car2 = {
        "model" : request.form.get('selected_model_c2'),
        "engine": request.form.get('selected_engine_c2'),
        "country": request.form.get('selected_country_c2'),
        "hd": request.form.get('selected_hd_c2'),
        "year": request.form.get('selected_year_c2')
    }

    #Get category values
    categories = request.form.get('category-list')
    if len(categories) < 1:
        categories = "emptyValue"

    sub_categories = request.form.get('sub-category-list')
    if len(sub_categories) < 1:
        sub_categories = "emptyValue"

    #Read DF and filter after category
    df_c1 = filter_for_car(car1, categories, sub_categories)
    df_c2 = filter_for_car(car2, categories, sub_categories)

    #Compare DataFrame
    df_compared = pd.DataFrame()
    for tn in df_c2.id:
        if len(df_c1[df_c1.id == tn]) == 0:
            df_compared = df_compared.append(df_c2[df_c2.id == tn])

    if (len(categories) > 0) or (len(sub_categories) > 0):
        return render_template('results.html',  tables=[df_compared.to_html()], titles=df_compared.columns.values, title=len(df_compared))
    elif (len(df_compared) == 0):
        return jsonify('No Results Found')
    else:
        return jsonify('Error Occured: Please chose atleast one category')


if __name__ == '__main__':
    app.run(debug=True)
