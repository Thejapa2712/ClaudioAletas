from flask import Flask, render_template, request, redirect, url_for
from modelo2 import calcular_eficiencia, mostrar_formula, gerar_grafico, salvar_resultados 
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import os
import datetime
import matplotlib
matplotlib.use('TkAgg')

app = Flask(__name__)

materiais = {
    1: {"nome": "Alumínio", "k": 205},
    2: {"nome": "Cobre", "k": 386},
    3: {"nome": "Aço Inoxidável", "k": 16},
    4: {"nome": "Latão", "k": 120},
    5: {"nome": "Titânio", "k": 21},
    6: {"nome": "Prata", "k": 429},
    7: {"nome": "Ouro", "k": 318},
    8: {"nome": "Ferro", "k": 80},
    9: {"nome": "Níquel", "k": 90},
    10: {"nome": "Chumbo", "k": 34},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tipos_aletas', methods=['GET', 'POST'])
def tipos_aletas():
    if request.method == 'POST':
        tipo_aleta = request.form['tipo_aleta']
        return redirect(url_for('aletas_formulas', tipo_aleta=tipo_aleta))
    return render_template('tipos_aletas.html')

@app.route('/aletas_formulas/<tipo_aleta>', methods=['GET', 'POST'])
def aletas_formulas(tipo_aleta):
    if request.method == 'POST':
        return redirect(url_for('tipos_materiais', tipo_aleta=tipo_aleta))
    imagem_aleta, formula_aleta = mostrar_formula(tipo_aleta)
    return render_template('aletas_formulas.html', tipo_aleta=tipo_aleta, imagem_aleta=imagem_aleta, formula_aleta=formula_aleta)

@app.route('/tipos_materiais/<tipo_aleta>', methods=['GET', 'POST'])
def tipos_materiais(tipo_aleta):
    if request.method == 'POST':
        material_id = int(request.form['material'])
        material = materiais[material_id]
        return redirect(url_for('inserir_dados', tipo_aleta=tipo_aleta, material=material['nome'], k=material['k']))
    return render_template('tipos_materiais.html', tipo_aleta=tipo_aleta, materiais=materiais)

@app.route('/inserir_dados/<tipo_aleta>/<material>/<k>', methods=['GET', 'POST'])
def inserir_dados(tipo_aleta, material, k):
    if request.method == 'POST':
        h = float(request.form['h'])
        T_b = float(request.form['T_b'])
        T_inf = float(request.form['T_inf'])

        if tipo_aleta in ["1)aletas retangulares retas", "2)aletas triangulares retas", "3)aletas parabolicas retas"]:
            l = float(request.form['l'])
            t = float(request.form['t'])
            w = float(request.form['w'])
            return redirect(url_for('resultado', tipo_aleta=tipo_aleta, material=material, h=h, k=k, l=l, t=t, w=w, T_b=T_b, T_inf=T_inf))
        
        elif tipo_aleta == "4)aletas circulares de perfil retangular":
            l = float(request.form['l'])
            r1 = float(request.form['r1'])
            r2 = float(request.form['r2'])
            w = float(request.form['w'])
            return redirect(url_for('resultado', tipo_aleta=tipo_aleta, material=material, h=h, k=k, l=l, r1=r1, r2=r2, w=w, T_b=T_b, T_inf=T_inf))
        
        else:
            l = float(request.form['l'])
            D = float(request.form['D'])
            return redirect(url_for('resultado', tipo_aleta=tipo_aleta, material=material, h=h, k=k, l=l, D=D, T_b=T_b, T_inf=T_inf))
    
    return render_template('inserir_dados.html', tipo_aleta=tipo_aleta, material=material, k=k)

@app.route('/resultado')
def resultado():
    tipo_aleta = request.args.get('tipo_aleta')
    material = request.args.get('material')
    h = float(request.args.get('h'))
    k = float(request.args.get('k'))
    l = float(request.args.get('l'))
    T_b = float(request.args.get('T_b'))
    T_inf = float(request.args.get('T_inf'))

    if tipo_aleta in ["1)aletas retangulares retas", "2)aletas triangulares retas", "3)aletas parabolicas retas"]:
        t = float(request.args.get('t'))
        w = float(request.args.get('w'))
        eta_aleta, Q_aleta, A_aleta = calcular_eficiencia(tipo_aleta, h, k, (l, t, w, None, None, None), T_b, T_inf)
        grafico_path = gerar_grafico(tipo_aleta, h, k, l, t, w, T_b, T_inf, A_aleta, material, eta_aleta, np.sqrt(2 * h / (k * t)))
    
    elif tipo_aleta == "4)aletas circulares de perfil retangular":
        r1 = float(request.args.get('r1'))
        r2 = float(request.args.get('r2'))
        w = float(request.args.get('w'))
        eta_aleta, Q_aleta, A_aleta = calcular_eficiencia(tipo_aleta, h, k, (l, r1, r2, w, None, None), T_b, T_inf)
        grafico_path = gerar_grafico(tipo_aleta, h, k, l, r1, r2, T_b, T_inf, A_aleta, material, eta_aleta, np.sqrt(2 * h / (k * w)))
    
    else:
        D = float(request.args.get('D'))
        eta_aleta, Q_aleta, A_aleta = calcular_eficiencia(tipo_aleta, h, k, (l, D, None, None, None, None), T_b, T_inf)
        grafico_path = gerar_grafico(tipo_aleta, h, k, l, D, T_b, T_inf, A_aleta, material, eta_aleta, np.sqrt(4 * h / (k * D)))

    # Salvar os resultados em um arquivo
    filepath = 'static/relatorio.txt'
    salvar_resultados(tipo_aleta, material, h, k, (l, None, None), T_b, T_inf, eta_aleta, Q_aleta, A_aleta, filepath)

    return render_template('resultado.html', eta_aleta=eta_aleta, Q_aleta=Q_aleta, tipo_aleta=tipo_aleta, material=material, grafico_path=grafico_path, relatorio_path=filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')