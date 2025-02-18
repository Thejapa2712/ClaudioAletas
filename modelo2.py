import matplotlib
matplotlib.use('TkAgg')

import sys
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkImage

from scipy.special import i0, i1, k0, k1, i0e, i1e
import scipy.special as sp
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import datetime

import torch

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

def escolher_aleta():
    def on_select():
        root.tipo_aleta = aleta_var.get()
        root.destroy()

    root = ctk.CTk()
    root.title("Escolha o tipo de aleta")

    # Tamanho da janela da escolha de Aletas
    root.geometry("500x400")

    aleta_var = ctk.StringVar(value="1)aletas retangulares retas")

    tipos = [
        "1)aletas retangulares retas",
        "2)aletas triangulares retas",
        "3)aletas parabolicas retas",
        "4)aletas circulares de perfil retangular",
        "5)aletas de perfil retangular",
        "6)aletas de perfil triangular",
        "7)aletas de perfil parabolico",
        "8)aletas de pino de perfilparabolico (ponta arredondada)"
    ]

    label = ctk.CTkLabel(root, text="Escolha o tipo de aleta:", font=("Arial", 20, "bold"))
    label.pack(pady=10)

    for tipo in tipos:
        radio = ctk.CTkRadioButton(root, text=tipo.replace('_', ' ').title(), variable=aleta_var, value=tipo, command=on_select, font=("Arial", 15, "bold"))
        radio.pack(anchor=ctk.W, pady=5)

    root.mainloop()

    return getattr(root, 'tipo_aleta', None)

def obter_imagem(tipo_aleta):
    imagens = {
        "1)aletas retangulares retas": "static/aletas/1.png",
        "2)aletas triangulares retas": "static/aletas/2.png",
        "3)aletas parabolicas retas": "static/aletas/3.png",
        "4)aletas circulares de perfil retangular": "static/aletas/4.png",
        "5)aletas de perfil retangular": "static/aletas/5.png",
        "6)aletas de perfil triangular": "static/aletas/6.png",
        "7)aletas de perfil parabolico": "static/aletas/7.png",
        "8)aletas de pino de perfilparabolico (ponta arredondada)": "static/aletas/8.png"
    }
    return imagens.get(tipo_aleta)

def obter_formula(tipo_aleta):
    formulas = {
        "1)aletas retangulares retas": "static/formulas/1.png",
        "2)aletas triangulares retas": "static/formulas/2.png",
        "3)aletas parabolicas retas": "static/formulas/3.png",
        "4)aletas circulares de perfil retangular": "static/formulas/4.png",
        "5)aletas de perfil retangular": "static/formulas/5.png",
        "6)aletas de perfil triangular": "static/formulas/6.png",
        "7)aletas de perfil parabolico": "static/formulas/7.png",
        "8)aletas de pino de perfilparabolico (ponta arredondada)": "static/formulas/8.png"
    }
    return formulas.get(tipo_aleta)

    root = ctk.CTk()
    root.title("Fórmula Utilizada")

    # Tamanho da janela das Imagens das formulas e das aletas
    root.geometry("800x900")

    label = ctk.CTkLabel(root, text=f" {tipo_aleta.replace('_', ' ').title()}:", justify=ctk.LEFT, font=("Arial", 20, "bold"))
    label.pack(pady=10, padx=20)

    img = None
    image_path = imagens.get(tipo_aleta)
    if image_path:
        img = Image.open(image_path)

        # Tamanho da Imagem do tipo de Aleta
        img = img.resize((600, 400), Image.LANCZOS)
    
        img = CTkImage(light_image=img, dark_image=img, size=(700, 400))
        panel = ctk.CTkLabel(root, image=img)
        panel.pack(side=ctk.TOP, padx=10, pady=10)

    formula_img = None
    formula_image_path = imagens_formulas.get(tipo_aleta)
    if formula_image_path:
        formula_img = Image.open(formula_image_path)

        # Tamanho da imagem das Formulas
        formula_img = formula_img.resize((600, 300), Image.LANCZOS)

        formula_img = CTkImage(light_image=formula_img, dark_image=formula_img, size=(700, 300))
        formula_panel = ctk.CTkLabel(root, image=formula_img)
        formula_panel.pack(side=ctk.TOP, padx=10, pady=10)

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    ok_button = ctk.CTkButton(button_frame, text="OK", command=root.destroy)
    ok_button.pack(side=ctk.LEFT, padx=5)

    back_button = ctk.CTkButton(button_frame, text="Voltar", command=lambda: [root.destroy(), main()])
    back_button.pack(side=ctk.LEFT, padx=5)

    root.mainloop()

    return img, formula_img

def escolher_material():
    def on_select():
        root.mat_tipo = int(material_var.get())
        root.destroy()

    def on_back():
        root.destroy()
        main()

    root = ctk.CTk()
    root.title("Escolha o material")

    # Tamanho da janela da escolha de material
    root.geometry("600x350")

    material_var = ctk.StringVar(value="1")

    materiais = {
        1: {"nome": "Alumínio", "k": 205},  # Pode variar entre 200-237 W/m·K
        2: {"nome": "Cobre", "k": 386},  
        3: {"nome": "Aço Inoxidável", "k": 16},  # Pode variar entre 14-20 W/m·K
        4: {"nome": "Latão", "k": 120},  
        5: {"nome": "Titânio", "k": 21}, 
        6: {"nome": "Prata", "k": 429}, 
        7: {"nome": "Ouro", "k": 318},  
        8: {"nome": "Ferro", "k": 80},  # Pode variar entre 50-80 W/m·K
        9: {"nome": "Níquel", "k": 90},  
        10: {"nome": "Chumbo", "k": 34},  
    }

    label = ctk.CTkLabel(root, text="Escolha o material levando em consideração sua Condutividade Térmica (W/mK):", font=("Arial", 16))
    label.pack(pady=10)

    for i, mat in materiais.items():
        radio = ctk.CTkRadioButton(root, text=f"{i}. {mat['nome']} -- {mat['k']} W/mK", variable=material_var, value=i, command=on_select, font=("Arial", 15))
        radio.pack(anchor=ctk.W)

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    back_button = ctk.CTkButton(button_frame, text="Voltar", command=on_back)
    back_button.pack(side=ctk.LEFT, padx=5)

    root.mainloop()

    mat_tipo = getattr(root, 'mat_tipo', None)
    return materiais[mat_tipo]["nome"], materiais[mat_tipo]["k"]

# Resto do código permanece o mesmo

def calcular_eficiencia(tipo_aleta, h, k, dimensoes, T_b, T_inf):
    theta_b = T_b - T_inf  

    if tipo_aleta == "1)aletas retangulares retas":
        l, t, w, _, _, _ = dimensoes
        m = np.sqrt(2 * h / (k * t))
        A_aleta = 2 * w * (l + t / 2)
        eta_aleta = np.tanh(m * (l + t / 2)) / (m * (l + t / 2))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "2)aletas triangulares retas":
        l, t, w, _, _, _ = dimensoes
        m = np.sqrt(2 * h / (k * t))
        A_aleta = 2 * w * np.sqrt(l**2 + (t / 2)**2)
        eta_aleta = (1 / (m * l)) * (sp.i1(2*m * l) / sp.i0(2*m * l))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "3)aletas parabolicas retas":
        l, t, w, _, _, _ = dimensoes
        m = np.sqrt(2 * h / (k * t))
        C1 = np.sqrt(1 + (t / l)**2)
        A_aleta = w * l * (C1 + (l / t) * np.log(t / l + C1))
        eta_aleta = 2 / (1 + np.sqrt((2 * m * l)**2 + 1))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "4)aletas circulares de perfil retangular":
        l, t, _, _, r1, r2 = dimensoes
        m = np.sqrt(2 * h / (k * t))
        A_aleta = 2 * np.pi * (r2**2 - r1**2)
        r2c = r2 + t / 2
        C2 = (2 * r1 / m) / (r2c**2 - r1**2)
        
        
        K1_mr1 = sp.k1(m * r1)
        I1_mr2c = sp.i1(m * r2c)
        I1_mr1 = sp.i1(m * r1)
        K1_mr2c = sp.k1(m * r2c)
        I0_mr1 = sp.i0(m * r1)
        K0_mr1 = sp.k0(m * r1)

       
        eta_aleta = C2 * ((K1_mr1 * I1_mr2c - I1_mr1 * K1_mr2c) /
                          (I0_mr1 * K1_mr2c + K0_mr1 * I1_mr2c))
        
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "5)aletas de perfil retangular":
        l, _, _, D, _, _ = dimensoes
        m = np.sqrt(4* h / (k * D))
        A_aleta = np.pi * D * (l + D / 4)
        eta_aleta = np.tanh(m * (l + D / 4)) / (m * (l + D / 4))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "6)aletas de perfil triangular":
        l, _, _, D, _, _ = dimensoes
        m = np.sqrt(4 * h / (k * D))
        A_aleta = (np.pi * D / 2) * np.sqrt(l**2 + (D / 2)**2)
        x = 2 * m * l
        I2_x = sp.i0(x) - (2 / x) * sp.i1(x)
        eta_aleta = (2 * I2_x) / (m * l * sp.i1(x))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "7)aletas de perfil parabolico":
        l, _, _, D, _, _ = dimensoes
        m = np.sqrt(4* h / (k * D))
        C3 = 1 + 2 * (D / l)**2
        C4 = np.sqrt(1 + (D / l)**2)
        A_aleta = (np.pi * l**3) / (8 * D) * (C3 * C4 - (l / (2 * D)) * np.log((2 * D * C4 / l + C3)))
        eta_aleta = 2 / (1 + np.sqrt((2 * m * l / 3)**2 + 1))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    elif tipo_aleta == "8)aletas de pino de perfilparabolico (ponta arredondada)":
        l, _, _, D, _, _ = dimensoes
        m = np.sqrt(4 * h / (k * D))
        A_aleta = (np.pi * D**4 / (96 * l**2)) * ((16 * (l / D)**2 + 1)**(3 / 2) - 1)
        eta_aleta = (3 / (2 * m * l)) * (sp.i1((4 * m * l / 3)) / sp.i0((4 * m * l / 3)))
        Q_aleta = eta_aleta * A_aleta * h * theta_b
        return eta_aleta, Q_aleta, A_aleta

    else:
        return None, None, None

import os
import datetime

def salvar_resultados(tipo_aleta, material, h, k, dimensoes, T_b, T_inf, eta_aleta, Q_aleta, A_aleta, filepath):
    relatorio = (
        f"Dados da Aleta:\n"
        f"Tipo de Aleta: {tipo_aleta}\n"
        f"Material: {material}\n"
        f"Coeficiente de transferência de calor (h): {h:.2f} W/m²K\n"
        f"Condutividade térmica (k): {k:.2f} W/mK\n"
        f"Dimensões: {dimensoes}\n"
        f"Temperatura do meio (T∞): {T_inf} °C\n"
        f"Temperatura da base da aleta (Tb): {T_b} °C\n"
        f"Eficiência: {eta_aleta:.6f}\n"
        f"Área da Aleta: {A_aleta:.6f} m²\n"
        f"Taxa de Transferência de Calor (Q_aleta): {Q_aleta:.6f} W\n"
    )
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(relatorio)

def gerar_grafico(tipo_aleta, h, k, l, t, w, T_b, T_inf, A_aleta, material, eta_aleta, m, save_path=None):
    x = np.linspace(0, l, 100)
    theta_b = T_b - T_inf

    if tipo_aleta in ["1)aletas retangulares retas", "2)aletas triangulares retas", "3)aletas parabolicas retas", "4)aletas circulares de perfil retangular"]:
        theta_x = theta_b * np.cosh(m * (l - x)) / np.cosh(m * l)
    else:
        theta_x = theta_b * np.cosh(m * (l - x)) / np.cosh(m * l)

    T_x = T_inf + theta_x

    plt.figure(figsize=(12, 8))  # Aumentar o tamanho do gráfico
    plt.plot(x, T_x, label="Distribuição de Temperatura", color="blue")

    plt.axvline(0.1 * l, color="gray", linestyle="--", linewidth=1, label="Limite Alta Transferência de Calor")
    plt.axvline(0.5 * l, color="gray", linestyle="--", linewidth=1, label="Limite Baixa Transferência de Calor")

    plt.text(0.05 * l, T_b + (T_inf - T_b) * (np.cosh(m * (l - 0.05 * l)) / np.cosh(m * l)), "Alta\ntransferência\nde calor", fontsize=10, color="black", ha="center")
    plt.text(0.3 * l, T_b + (T_inf - T_b) * (np.cosh(m * (l - 0.3 * l)) / np.cosh(m * l)), "Baixa\ntransferência\nde calor", fontsize=10, color="black", ha="center")
    plt.text(0.75 * l, T_b + (T_inf - T_b) * (np.cosh(m * (l - 0.75 * l)) / np.cosh(m * l)), "Muito Baixa\ntransferência\nde calor", fontsize=10, color="black", ha="center")

    info_text = (f"Tipo de Aleta: {tipo_aleta} (Ponta Adiabática)\n"
                 f"Material: {material}\n"
                 f"Coeficiente de transferência de calor (h): {h:.2f} W/m²K\n"
                 f"Condutividade térmica (k): {k:.2f} W/mK\n"
                 f"Eficiência: {eta_aleta:.6f}\n"
                 f"Área da Aleta: {A_aleta:.6f} m²\n"
                 f"Taxa de Transferência de Calor (Q_aleta): {eta_aleta * A_aleta * h * theta_b:.6f} W")
    plt.legend([info_text], loc="upper right", fontsize=12)
    if save_path:
        plt.savefig(save_path)
    else:
        grafico_path = 'static/grafico.png'
        plt.savefig(grafico_path)
    plt.xlabel("Comprimento (m)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Distribuição de Temperatura ao Longo da Aleta")
    plt.grid()
    plt.close()
    return grafico_path

def mostrar_formula(tipo_aleta):
    imagem_aleta = obter_imagem(tipo_aleta)
    formula_aleta = obter_formula(tipo_aleta)
    return imagem_aleta, formula_aleta

def on_save(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta):
    output_dir = "D:/Trabalho/Resultados"
    os.makedirs(output_dir, exist_ok=True)
    results_filepath = os.path.join(output_dir, f"resultados_{tipo_aleta.replace(' ', '_')}.txt")
    salvar_resultados(tipo_aleta, material, h, k, (l, t, w, D, r1, r2), T_b, T_inf, eta_aleta, Q_aleta, A_aleta, results_filepath)
    graph_filepath = os.path.join(output_dir, f"grafico_{tipo_aleta.replace(' ', '_')}.png")
    gerar_grafico(tipo_aleta, h, k, l, t, w, T_b, T_inf, A_aleta, material, eta_aleta, np.sqrt(2 * h / (k * t)), save_path=graph_filepath)

def mostrar_janela_salvamento(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta):
    root = ctk.CTk()
    root.title("Salvar ou Cancelar")
    root.geometry("300x150")

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20)

    save_button = ctk.CTkButton(button_frame, text="Salvar Dados", command=lambda: [on_save(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta), root.destroy()])
    save_button.pack(side=ctk.LEFT, padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=root.destroy)
    cancel_button.pack(side=ctk.LEFT, padx=10)

    root.mainloop()

def on_submit(h_entry, l_entry, t_entry, w_entry, D_entry, r1_entry, r2_entry, T_inf_entry, T_b_entry, error_label, root):
    try:
        h = float(h_entry.get())
        l = float(l_entry.get())
        t = float(t_entry.get()) if t_entry else None
        w = float(w_entry.get()) if w_entry else None
        D = float(D_entry.get()) if D_entry else None
        r1 = float(r1_entry.get()) if r1_entry else None
        r2 = float(r2_entry.get()) if r2_entry else None
        T_inf = float(T_inf_entry.get())
        T_b = float(T_b_entry.get())
        if h > 0 and l > 0 and (t is None or t > 0) and (w is None or w > 0) and (D is None or D > 0) and (r1 is None or r1 > 0) and (r2 is None or r2 > 0):
            root.h = h
            root.l = l
            root.t = t
            root.w = w
            root.D = D
            root.r1 = r1
            root.r2 = r2
            root.T_inf = T_inf
            root.T_b = T_b
            root.destroy()
        else:
            error_label.config(text="Erro: Todos os valores devem ser números positivos.")
    except ValueError:
        error_label.config(text="Erro: Certifique-se de inserir números válidos.")


def on_save(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta,):
    output_dir = "D:/Trabalho/Resultados"
    os.makedirs(output_dir, exist_ok=True)
    results_filepath = os.path.join(output_dir, f"resultados_{tipo_aleta.replace(' ', '_')}.txt")
    salvar_resultados(tipo_aleta, material, h, k, (l, t, w, D, r1, r2), T_b, T_inf, eta_aleta, Q_aleta, A_aleta, results_filepath)
    graph_filepath = os.path.join(output_dir, f"grafico_{tipo_aleta.replace(' ', '_')}.png")
    gerar_grafico(l, tipo_aleta, material, h, k, np.sqrt(2 * h / (k * t)), eta_aleta, T_inf, T_b, A_aleta, save_path=graph_filepath)

def mostrar_janela_salvamento(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta):
    root = ctk.CTk()
    root.title("Salvar ou Cancelar")
    root.geometry("300x150")

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20)

    save_button = ctk.CTkButton(button_frame, text="Salvar Dados", command=lambda: [on_save(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta), root.destroy()])
    save_button.pack(side=ctk.LEFT, padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=root.destroy)
    cancel_button.pack(side=ctk.LEFT, padx=10)

    root.mainloop()

def main():
    tipo_aleta = escolher_aleta()
    img, formula_img = mostrar_formula(tipo_aleta)
    material, k = escolher_material()

    root = ctk.CTk()
    root.title("Insira os valores")
     #Tamanho da janela que são inserisos os valores
    root.geometry("650x350")

    frame = ctk.CTkFrame(root)
    frame.pack(pady=10)

    ctk.CTkLabel(frame, text="Coeficiente de transferência de calor (h) (W/m²K):").grid(row=0, column=0, padx=5, pady=5, sticky=ctk.W)
    h_entry = ctk.CTkEntry(frame)
    h_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Comprimento (l) (m):").grid(row=1, column=0, padx=5, pady=5, sticky=ctk.W)
    l_entry = ctk.CTkEntry(frame)
    l_entry.grid(row=1, column=1, padx=5, pady=5)

    if tipo_aleta in ["1)aletas retangulares retas", "2)aletas triangulares retas", "3)aletas parabolicas retas"]:
        ctk.CTkLabel(frame, text="Espessura (t) (m):").grid(row=2, column=0, padx=5, pady=5, sticky=ctk.W)
        t_entry = ctk.CTkEntry(frame)
        t_entry.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame, text="Largura (w) (m):").grid(row=3, column=0, padx=5, pady=5, sticky=ctk.W)
        w_entry = ctk.CTkEntry(frame)
        w_entry.grid(row=3, column=1, padx=5, pady=5)
        D_entry = None
        r1_entry = None
        r2_entry = None
    elif tipo_aleta == "4)aletas circulares de perfil retangular":
        ctk.CTkLabel(frame, text="Raio interno (r1) (m):").grid(row=2, column=0, padx=5, pady=5, sticky=ctk.W)
        r1_entry = ctk.CTkEntry(frame)
        r1_entry.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame, text="Raio externo (r2) (m):").grid(row=3, column=0, padx=5, pady=5, sticky=ctk.W)
        r2_entry = ctk.CTkEntry(frame)
        r2_entry.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(frame, text="Espessura (t) (m):").grid(row=4, column=0, padx=5, pady=5, sticky=ctk.W)
        t_entry = ctk.CTkEntry(frame)
        t_entry.grid(row=4, column=1, padx=5, pady=5)
        w_entry = None
        D_entry = None
    else:
        ctk.CTkLabel(frame, text="Diâmetro (D) (m):").grid(row=2, column=0, padx=5, pady=5, sticky=ctk.W)
        D_entry = ctk.CTkEntry(frame)
        D_entry.grid(row=2, column=1, padx=5, pady=5)
        t_entry = None
        w_entry = None
        r1_entry = None
        r2_entry = None

    ctk.CTkLabel(frame, text="Temperatura do meio (T∞) (°C):").grid(row=5, column=0, padx=5, pady=5, sticky=ctk.W)
    T_inf_entry = ctk.CTkEntry(frame)
    T_inf_entry.grid(row=5, column=1, padx=5, pady=5)

    ctk.CTkLabel(frame, text="Temperatura da base da aleta (Tb) (°C):").grid(row=6, column=0, padx=5, pady=5, sticky=ctk.W)
    T_b_entry = ctk.CTkEntry(frame)
    T_b_entry.grid(row=6, column=1, padx=5, pady=5)

    error_label = ctk.CTkLabel(frame, text="", text_color="red")
    error_label.grid(row=7, column=0, columnspan=2, pady=5)

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    submit_button = ctk.CTkButton(button_frame, text="Confirmar", command=lambda: on_submit(h_entry, l_entry, t_entry, w_entry, D_entry, r1_entry, r2_entry, T_inf_entry, T_b_entry, error_label, root))
    submit_button.pack(side=ctk.LEFT, padx=5)

    back_button = ctk.CTkButton(button_frame, text="Voltar", command=lambda: [root.destroy(), main()])
    back_button.pack(side=ctk.LEFT, padx=5)

    root.mainloop()
    # Aqui salva os valores que foram digitados
    h = getattr(root, 'h', None)
    l = getattr(root, 'l', None)
    t = getattr(root, 't', None)
    w = getattr(root, 'w', None)
    D = getattr(root, 'D', None)
    r1 = getattr(root, 'r1', None)
    r2 = getattr(root, 'r2', None)
    T_inf = getattr(root, 'T_inf', None)
    T_b = getattr(root, 'T_b', None)

    if h is None or l is None or T_inf is None or T_b is None or (t is None and w is None and D is None and r1 is None and r2 is None):
        print("Valores não fornecidos.")
        return

    dimensoes = (l, t, w, D, r1, r2)
    eta_aleta, Q_aleta, A_aleta = calcular_eficiencia(tipo_aleta, h, k, dimensoes, T_b, T_inf)

     # Aqui mostra a Area da Aleta na legenda do Grafico 
    if eta_aleta is not None and Q_aleta is not None:
        if tipo_aleta in ["1)aletas retangulares retas", "2)aletas triangulares retas", "3)aletas parabolicas retas", "4)aletas circulares de perfil retangular"]:
            m = np.sqrt(2 * h / (k * t))
            if tipo_aleta == "1)aletas retangulares retas":
                A_aleta = 2 * w * (l + t / 2)
            elif tipo_aleta == "2)aletas triangulares retas":
                A_aleta = 2 * w * np.sqrt(l**2 + (t / 2)**2)
            elif tipo_aleta == "3)aletas parabolicas retas":
                C1 = np.sqrt(1 + (t / l)**2)
                A_aleta = w * l * (C1 + (l / t) * np.log(t / l + C1))
            elif tipo_aleta == "4)aletas circulares de perfil retangular":
                A_aleta = 2 * np.pi * (r2**2 - r1**2)
        else:
            m = np.sqrt(4 * h / (k * D))
            if tipo_aleta == "5)aletas de perfil retangular":
                A_aleta = np.pi * D * (l + D / 4)
            elif tipo_aleta == "6)aletas de perfil triangular":
                A_aleta = (np.pi * D / 2) * np.sqrt(l**2 + (D / 2)**2)
            elif tipo_aleta == "7)aletas de perfil parabolico":
                C3 = 1 + 2 * (D / l)**2
                C4 = np.sqrt(1 + (D / l)**2)
                A_aleta = (np.pi * l**3) / (8 * D) * (C3 * C4 - (l / (2 * D)) * np.log((2 * D * C4 / l + C3)))
            elif tipo_aleta == "8)aletas de pino de perfilparabolico (ponta arredondada)":
                A_aleta = (np.pi * D**4 / (96 * l**2)) * ((16 * (l / D)**2 + 1)**(3 / 2) - 1)

        gerar_grafico(tipo_aleta, h, k, l, t, w, T_b, T_inf, A_aleta, material, eta_aleta, m)
        mostrar_janela_salvamento(h, l, t, w, D, r1, r2, T_inf, T_b, tipo_aleta, material, k, eta_aleta, Q_aleta, A_aleta)
    else:
        print("Erro ao calcular a eficiência da aleta.")

if __name__ == "__main__":
    main()
