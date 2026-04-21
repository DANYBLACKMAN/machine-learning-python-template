#from utils import db_connect
#engine = db_connect()

# your code here
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# 1. Cargar el modelo guardado (asumiendo que ejecutas desde la raíz del proyecto)
modelo = pickle.load(open('models/nba_model.sav', 'rb'))

# 2. Un diccionario para que el resultado en pantalla sea fácil de entender
nombres_posiciones = {
    'G': 'Guard (Base / Escolta)',
    'F': 'Forward (Alero / Ala-Pívot)',
    'C': 'Center (Pívot)'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediccion = None

    if request.method == 'POST':
        # 3. Capturar los números que el usuario escribirá en la web
        mpg = float(request.form['mpg'])
        tpa = float(request.form['tpa'])
        tpp = float(request.form['tpp'])
        ppg = float(request.form['ppg'])
        rpg = float(request.form['rpg'])
        apg = float(request.form['apg'])
        spg = float(request.form['spg'])
        bpg = float(request.form['bpg'])

        # 4. Agrupar los datos en el MISMO ORDEN en que entrenamos el modelo
        datos_ingresados = [[mpg, tpa, tpp, ppg, rpg, apg, spg, bpg]]
        
        # 5. Hacer la predicción
        resultado_crudo = modelo.predict(datos_ingresados)[0]
        prediccion = nombres_posiciones[resultado_crudo]

    # 6. Enviar la respuesta a la página web
    return render_template('index.html', resultado_final=prediccion)

if __name__ == '__main__':
    # Arrancamos el servidor local
    app.run(debug=True, host='0.0.0.0', port=8080)
