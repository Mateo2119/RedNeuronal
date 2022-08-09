from urllib import request
from flask import Flask, render_template, request, url_for, redirect, send_file
from logic import RedNeuronal

app = Flask(__name__,template_folder='plantillas')
miRed = RedNeuronal()

@app.route('/')
def index():    
    miRed.iniciar()
    return render_template('index.html')

@app.route('/information')
def info():    
    return render_template('info.html')

@app.route('/dispertion')
def disp():
    grafica = miRed.graficar()
    return grafica


@app.route('/analizar',methods=['POST'])
def analizar():
    if request.method == 'POST':
        mama = int(request.form['qualy_Mom'])
        papa = int(request.form['qualy_Dad'])
        miRed.entrenar()
        miRed.predecir(mama,papa)
        return redirect(url_for('results'))
    return redirect(url_for('index'))

@app.route('/results')
def results():
    puntaje = str(miRed.puntajeR)
    prediccion = str(miRed.prediccion)
    correlacion = miRed.correlacion
    return render_template('resultados.html', puntaje=puntaje[0:4], prediccion = prediccion[1:5], corr=correlacion)



if __name__=='__main__':
    app.run(debug=True)