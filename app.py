import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file

app = Flask(__name__)

# Function to fetch data from the database
def get_dopants():
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Dopant FROM FormEnData")
    dopants = cursor.fetchall()
    conn.close()
    return [dopant[0] for dopant in dopants]

def get_host_material(selected_material):
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    # cursor.execute("SELECT DISTINCT Dopant FROM F_NN_Output_data WHERE Dopant Like %_"+selected_material)
    query = "SELECT DISTINCT Dopant FROM F_NN_Output_data WHERE Dopant LIKE ?"
    # Construct the pattern with the selected_material variable
    pattern = "%" + "_" + selected_material
    cursor.execute(query, (pattern,))
    dopants = cursor.fetchall()
    conn.close()
    return [dopant[0] for dopant in dopants]

def get_elements():
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Element FROM bandgap21")
    elements = cursor.fetchall()
    conn.close()
    return [element[0] for element in elements]





@app.route('/')
def home():
    return render_template('home.html')

@app.route('/formation_energy', methods=['GET', 'POST'])
def formation_energy():
    dopants = get_dopants()
    model_options = ['GPR', 'NN', 'RFR']  # Options for the model dropdown menu
    
    # Fetch menu options for VASP files
    menu_options = get_vaspfile()

    if request.method == 'POST':
        selected_dopant = request.form['dopant']
        selected_model = request.form['model']
        print("Selected dopant:", selected_dopant)  
        print("Selected model:", selected_model)  
        formation_energy_value = get_formation_energy(selected_dopant, selected_model)
        print("Formation energy value:", formation_energy_value)  
        file_name_selected = request.form.get('option')  # Ensure to retrieve the selected option
        return render_template('formation_energy.html', dopants=dopants, model_options=model_options,
                               selected_dopant=selected_dopant, selected_model=selected_model,
                               formation_energy_value=formation_energy_value, menu_options=menu_options,
                               option=file_name_selected)
    return render_template('formation_energy.html', dopants=dopants, model_options=model_options,
                           menu_options=menu_options)



def get_vaspfile():
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Element FROM bandgap21")
    vaspfiles = cursor.fetchall()
    conn.close()
    return [vaspfile[0] for vaspfile in vaspfiles]

@app.route('/vasp', methods=['GET'])
def vasp():
    menu_options = get_vaspfile()
    option = request.args.get('option')
    if option in menu_options:
        file_name = option + ".vasp"
        return send_file(file_name, as_attachment=True)
    else:
        return "Option not found"
    
def get_formation_energy(dopant, model):
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    if model == 'GPR':
        cursor.execute("SELECT `Formation Energy GPR` FROM FormEnData WHERE Dopant = ?", (dopant,))
    elif model == 'RFR':
        cursor.execute("SELECT `Formation Energy RFR` FROM FormEnData WHERE Dopant = ?", (dopant,))
    elif model == 'NN':
        cursor.execute("SELECT `Formation Energy NN` FROM FormEnData WHERE Dopant = ?", (dopant,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "No data available for the selected dopant and model"

def get_host_materiall(dopant, model):
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    if model == 'GPR':
        cursor.execute("SELECT `GPR` FROM F_NN_Output_data WHERE Dopant = ?", (dopant,))
    elif model == 'RFR':
        cursor.execute("SELECT `RFR` FROM F_NN_Output_data WHERE Dopant = ?", (dopant,))
    elif model == 'NN':
        cursor.execute("SELECT `NN` FROM F_NN_Output_data WHERE Dopant = ?", (dopant,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "No data available for the selected dopant and model"

@app.route('/bandgap', methods=['GET', 'POST'])
def bandgap():
    elements = get_elements()
    model_options = ['GPR', 'NN', 'RFR']
    if request.method == 'POST':
        selected_element = request.form['element']
        selected_model = request.form['model']
        bandgap_value = get_bandgap(selected_element, selected_model)
        return render_template('bandgap.html', elements=elements, model_options=model_options,
                               selected_element=selected_element, selected_model=selected_model,
                               bandgap_value=bandgap_value)
    return render_template('bandgap.html', elements=elements, model_options=model_options)

def get_bandgap(element, model):
    conn = sqlite3.connect('perov21.db')
    cursor = conn.cursor()
    if model == 'GPR':
        cursor.execute("SELECT `Bandgap GPR` FROM bandgap21 WHERE Element = ?", (element,))
    elif model == 'NN':
        cursor.execute("SELECT `Bandgap NN` FROM bandgap21 WHERE Element = ?", (element,))
    elif model == 'RFR':
        cursor.execute("SELECT `Bandgap rfr` FROM bandgap21 WHERE Element = ?", (element,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "No data available for the selected element and model"
    
@app.route('/host_material', methods=['GET', 'POST'])
def host_material():
    
    materials = ['Cs','Sn']
    model_options = ['GPR', 'NN', 'RFR']  # Options for the model dropdown menu
    
    # # Fetch menu options for VASP files
    # menu_options = get_vaspfile()
    # selected_material = 'Cs'
    # dopants = get_host_material(selected_material)
    if request.method == 'POST':
        # selected_dopant = request.form['dopant']
        # selected_model = request.form['model']
        selected_material = request.form['materials']
        # print("Selected dopant:", selected_dopant)  
        # print("Selected model:", selected_model)  
        print("Selected material:", selected_material)
        # dopants = get_host_material(selected_material)
        # formation_energy_value = get_host_materiall(selected_dopant, selected_model)
        # print("Formation energy value:", formation_energy_value)  
        # file_name_selected = request.form.get('option')  # Ensure to retrieve the selected option
        # return render_template('host_material.html', materials = materials, selected_material=selected_material,
                            #    option=file_name_selected)
        print("line 170", selected_material)
        return redirect(url_for('material_specific', materiall=selected_material))
    return render_template('host_material.html', materials = materials)
    
@app.route('/material_specific/<materiall>', methods=['GET', 'POST'])
def material_specific(materiall):
    
    materials = ['Cs','Sn']
    model_options = ['GPR', 'NN', 'RFR']  # Options for the model dropdown menu
    
    # # Fetch menu options for VASP files
    # menu_options = get_vaspfile()
    selected_material = materiall
    dopants = get_host_material(materiall)
    if request.method == 'POST':
        selected_dopant = request.form['dopant']
        selected_model = request.form['model']
        print("Selected dopant:", selected_dopant)  
        print("Selected model:", selected_model)  
        print("Selected material:", selected_material)
        formation_energy_value = get_host_materiall(selected_dopant, selected_model)
        print("Formation energy value:", formation_energy_value)  
        file_name_selected = request.form.get('option')  # Ensure to retrieve the selected option
        return render_template('material_specific.html', materials = materials,dopants=dopants, model_options=model_options,
                               selected_dopant=selected_dopant, selected_model=selected_model, selected_material=selected_material,
                               formation_energy_value=formation_energy_value,
                               option=file_name_selected)
    return render_template('material_specific.html', dopants=dopants, model_options=model_options)

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
