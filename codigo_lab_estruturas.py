# Bibliotecas:

from tkinter import *
from PIL import Image
import math
import urllib.request
import json
import time
import requests
import json
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import os
from PIL import ImageTk, Image



# Foto geral:

im = Image.open('geral.png')
im.show()  

# Interface geral:

janela = Tk()
janela.title('Laboratório de estruturas - FEG')
janela.geometry("950x800")
janela['background'] = 'grey'


# Orientação:

texto_orientacao = Label(janela, text='Obs: Sempre utilize "." em vez de "," como separador decimal!', bg='#add8e6', font=("Arial", 12),fg='black')    
texto_orientacao.place(x=15, y=750)          

# Foto de saudação:

frame = Frame(janela, width=20, height=20, bg= 'grey')
frame.pack()
frame.place(x=110,y=20)
img = ImageTk.PhotoImage(Image.open("unesp_logo.png"))
label = Label(frame, image = img, bg='grey')
label.pack()

# 1) Treliça plana:
# resultado -> Deflexão do ponto C da treliça 
# p -> Carga aplicada no ponto C


def deflexao_trelica_plana():
    
    # Título:
    
    lb = Label(janela, text ="TRELIÇA PLANA:", anchor = W, fg = 'black',bg='blue')
    lb.place(x=510,y=20)

    # Dados de entrada (interface):

    Label(janela, text = 'Insira o valor da carga aplicada ao ponto C da treliça em Newtons:', anchor = W).place(x=510,y=50)
    p = Entry(janela)
    p.place(x=510, y=70)
    lb = Label(janela, text="Resultado:")
    lb.place(x=510, y=130)
    
    # Cálculo para saída:

    def bt_onclick():
        resultado = float(p.get())*1.0151*pow(10,-6)*1000
        lb["text"] = "De acordo com o Teorma de Castigliano, a deflexão teórica no ponto \nC é de {:.2f} mm".format(resultado)

    # Botão "Ok (interface)" 
    
    bt = Button(janela, text='Ok', command = bt_onclick)
    bt.place(x=510,y=100)

# 2) Vaso De Pressão: 

# TVP-> Tensão no vaso de pressão
# TTVP-> Tensão Tangencial no vaso de pressão
# TLVP-> Tensão Longitudinal no vaso de pressão
# p -> Pressão interna
# r -> raio
# t -> expessura (10% menor que o raio interno) 

def vaso_de_pressão(): 

    # Título:
    
    Label(janela, text = 'VASO DE PRESSÃO:', fg = 'black',bg='yellow').place(x=510, y=305)

    # Dados de entrada (interface):

    Label(janela, text = 'Insira a pressão interna P do vaso de pressão em MPa:', anchor = W).place(x=510,y=335)
    p = Entry(janela)
    p.place(x=510, y=355)
    Label(janela, text = 'Insira o raio interno R do vaso de presão em metros:', anchor = W).place(x=510,y=385)
    r = Entry(janela)
    r.place(x=510, y=405)
    Label(janela, text = 'Insira a espressura do vaso de pressão em centímetros:', anchor = W).place(x=510,y=435)
    t = Entry(janela)
    t.place(x=510, y=455)
    lb = Label(janela, text="Resultado:")
    lb.place(x=510, y=515)

    # Resultado de saída:
    
    def bt_onclick():
        TVP = (float(p.get())*float(r.get()))/(2*(float(t.get()))) + 0.2*(float(p.get()))      
        TTVP = (float(p.get())*float(r.get())) + 0.6*(float(p.get())) 
        TLVP = (float(p.get())*float(r.get()))/(2*(float(t.get()))) + 0.6*(float(p.get()))
        lb["text"] = 'Valores corrigidos de acordo com a norma ASME (2015):\nTensão no costado = {:.2f} MPa \nTensão tangencial no vaso de pressão = {:.2f} MPa \nTensão longitudinal no vaso de pressão: {:.2f} MPa'.format(TVP, TTVP, TLVP)

    # Botão "Ok":
    
    bt = Button(janela, text='Ok', command = bt_onclick)
    bt.place(x=510,y=485)

# 3) Tubo de tensões principais: 

# m -> Massa pendurada
# Mx-> Momento em x
# Iy-> Momento de inércia 
# Jy-> Momento polar de inércia em y
# Txy-> Tensão de cisalhamento xy

def tensões_e_deformações_tubo():

    # Título:
    
    Label(janela, text = 'TUBO DE TENSÕES PRINCIPAIS:',fg = 'black',bg='green').place(x=80,y=305)

    # Dados de entrada (interface):

    Label(janela, text = 'Insira a massa peso que será pendurada no dispositivo em Kg:', anchor = W).place(x=80,y=335)
    m = Entry(janela)
    m.place(x=80,y=355)
    
    lb = Label(janela, text="Resultado:")
    lb.place(x=80,y=415)

    def bt_onclick():
        
        # Tensões teóricas
        
        E = 200*pow(10,3)
        v = 0.3
        Iy = 1.1676*(pow(10,(-7)))
        J = (3.14/32)*(pow(0.064,4)-pow(0.0614,4))
        Mx = (float(m.get()))*10*0.40
        T = (float(m.get()))*10*0.42
        Iz = (3.14/64)*(pow(0.064,4)-pow(0.0614,4))
        Gx = (Mx*0.032)/Iz              
        Gy = float(0)
        Txy = (T*0.032)/J
        G_med = (Gx+Gy)/2
        dif = Gx - G_med
        R = pow((pow(Txy,2)+pow(dif,2)),0.5)
        T_max = R
        T_min = -R
        G_max = G_med + R
        G_min = G_med - R
        sen_dois_teta = Txy/R
        CF = Gx - G_med
        tg_dois_teta = Txy/CF
        dois_teta = (math.atan(tg_dois_teta))*(180/3.14)
        teta = dois_teta/2

        # Deformações Teóricas:

        e_max = (G_max - v*G_min)/E
        e_min = -(-v*G_max + G_min )/E



        lb["text"] ='Tensões Teóricas:\n\n\u03C3y = {} MPa\n\u03C3x = {:.2f} MPa\n\u03C3méd = {:.2f} Mpa\n\u03C3máx = {:.2f} Mpa\n\u03C3mín = {:.2f} Mpa\n\u03A4máx = {:.2f} Mpa\n\u03A4mín = {:.2f} Mpa\n\u03A4xy = {:.2f} Mpa \n\u03F4 = {:.2f}°\n\nDeformações Teóricas:\n\nεmáx = {:.2f} μm/m\nεmín = {:.2f} μm/m'.format(float(Gy),float(Gx)*pow(10,-6),float(G_med)*pow(10,-6),float(G_max)*pow(10,-6),float(G_min)*pow(10,-6),float(T_max)*pow(10,-6),float(T_min)*pow(10,-6),float(Txy)*pow(10,-6),float(teta),float(e_max),float(e_min)*(-1))



    # Botão "Ok":

    bt = Button(janela, text='Ok', command = bt_onclick)
    bt.place(x=80,y=385) 


# 4-) Viga hiperestática:

def deflexao_viga_hiperestatica():
    
    global lb1
    lb1 = Label(janela, text="Resultado:")
    lb1.place(x=900, y=765)

    # Botão para visualizar a representação esquemática da viga

    def foto_viga_hip():
     im = Image.open('viga_hiperestatica.jpg')
     return im.show()  
   
    bt_viga_hip = Button(janela, text='Ver esquema da viga',fg = 'black',bg='#ff6961', command = foto_viga_hip)
    bt_viga_hip.place(x=1180,y=305)

    global p1
    global p2
    global p3
    global p4
    global f1
    global f2
    global co
    global m1
    
    p1 = StringVar()
    p2 = StringVar()
    p3 = StringVar()
    p4 = StringVar()
    f1 = StringVar()
    f2 = StringVar()
    co = StringVar()
    m1 = StringVar()


    # Título:
    
    Label(janela, text = 'VIGA HIPERESTÁTICA: (conecte-se à internet)',fg = 'black',bg='#ff6961').place(x=900,y=305)
 

    # Entrada de dados
    Label(janela, text = 'Insira a posição da força em metros do momento concentrado (AD). Caso ela não exista, insira 0:', anchor = W).place(x=900,y=335)
    p1_amount = Entry(janela, textvariable = p1)
    p1_amount.place(x=900, y=355)

    Label(janela, text = 'Insira a força (em Newtons positiva ou negativa) que gera o momento concentrado (AD). Caso ela não exista, insira 0:', anchor = W).place(x=900,y=385)
    f1_amount = Entry(janela, textvariable = f1)
    f1_amount.place(x=900, y=405)

    Label(janela, text = 'Insira o momento concentrado (em N.m neg. p/ horário e pos. para anti-horário). Caso ele não exista, insira 0:', anchor = W).place(x=900,y=435)
    m1_amount = Entry(janela, textvariable= m1)
    m1_amount.place(x=900, y=455)

    Label(janela, text = 'Insira a posição da segunda força em metros (AF). Caso ela não exista, insira 0:', anchor = W).place(x=900,y=485)
    p2_amount = Entry(janela, textvariable= p2)
    p2_amount.place(x=900, y=505)

    Label(janela, text = 'Insira a a segunda força concentrada (em N/m positiva ou negativa). Caso ela não exista, insira 0:', anchor = W).place(x=900,y=535)
    f2_amount = Entry(janela, textvariable = f2)
    f2_amount.place(x=900, y=555)

    Label(janela, text = 'Insira em metros onde o carregamento começa (AB). Caso ele não exista, insira 0:', anchor = W).place(x=900,y=585)
    p3_amount = Entry(janela, textvariable= p3)
    p3_amount.place(x=900, y=605)

    Label(janela, text = 'Insira o valor do carregamento (em N/m negativo ou positivo). Caso ele não exista, insira 0:', anchor = W).place(x=900,y=635)
    co_amount = Entry(janela, textvariable = co)
    co_amount.place(x=900, y=655)

    Label(janela, text = 'Insira em metros onde o carregamento termina (AC).Caso ele não exista, insira 0:', anchor = W).place(x=900,y=685)
    p4_amount = Entry(janela, textvariable = p4)
    p4_amount.place(x=900, y=705)

    # Botão "Ok":
    
    bt = Button(janela, text='Ok', command = do_put)
    bt.place(x=900,y=735)

# Funções necessárias

def get_loads(force1_position, force1_mod,  moment_position, moment_value, force2_position, force2_mod, force_distributed_pos, force_distributed_mod, force_distributed_pos2, force_distributed_mod2):
        return [
                {
                    'id': 'T-tlp7OuTL-Epd0dpSi7vQ',
                    'type': 'fixed',
                    'label': 'Engastamento',
                    'position': {
                        'value': 0,
                        'display': '0',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.ky3ESg{stroke:rgba(72,72,72,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M19.5,4.8L19.5,39.2 M24.5,4.8L24.5,39.2 M19.5,4.8L24.5,9.7 M19.5,9.7L24.5,14.6 M19.5,14.6L24.5,19.5 M19.5,19.5L24.5,24.5 M19.5,24.5L24.5,29.4 M19.5,29.4L24.5,34.3 M19.5,34.3L24.5,39.2\' class=\'ky3ESg load _\'/></svg>',
                },
                {
                    'id': '4d5e8d63-6443-4af1-849d-11e7648bb03c',
                    'type': 'force',
                    'label': 'Carga concentrada',
                    'position': {
                        'value': force1_position,
                        'display': '0.3',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'magnitude': {
                        'value': force1_mod,
                        'display': '-41.8',
                        'units': 'N',
                        'unitsKey': 'newton',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.eRimDg{stroke:rgba(112,150,182,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M22,32.5L22,10.6 M18.6,26.7L22,32.5L25.4,26.7\' class=\'eRimDg load _\'/></svg>',
                },
                {
                    'id': '2957a888-1685-45db-8fc6-342b98056ea3',
                    'type': 'moment',
                    'label': 'Momento',
                    'position': {
                        'value': moment_position,
                        'display': '0.3',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'magnitude': {
                        'value': moment_value,
                        'display': '-1.56',
                        'units': 'N-m',
                        'unitsKey': 'newton-meter',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.eRimDg{stroke:rgba(112,150,182,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M29.1,7.6A16 16,0,0,1,19.7 37.9 M25.4,42.2L19.7,37.9L24.9,32.8 M14.9,36.4A16 16,0,0,1,24.3 6.1 M18.6,1.8L24.3,6.1L19.1,11.2\' class=\'eRimDg load _\'/></svg>',
                },
                {
                    'id': 'uQGZd_A5Q0uZ36EgxqX4yw',
                    'type': 'pin',
                    'label': 'Apoio simple',
                    'position': {
                        'value': 0.5,
                        'display': '0.5',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.ky3ESg{stroke:rgba(72,72,72,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M19.3,22a2.75,2.75 0 1,0 5.49,0a2.75,2.75 0 1,0 -5.5,0\' class=\'ky3ESg load _\'/><path d=\'M36.9,30.6L7.1,30.6L22,4.8L36.9,30.6\' class=\'ky3ESg load _\'/></svg>',
                },
                {
                    'id': 'fee94754-9755-4474-a316-6362298bd5b7',
                    'type': 'force',
                    'label': 'Carga concentrada',
                    'position': {
                        'value': force2_position,
                        'display': '0.6',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'magnitude': {
                        'value': force2_mod,
                        'display': '-51.2',
                        'units': 'N',
                        'unitsKey': 'newton',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.eRimDg{stroke:rgba(112,150,182,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M22,32.5L22,10.6 M18.6,26.7L22,32.5L25.4,26.7\' class=\'eRimDg load _\'/></svg>',
                },
                {
                    'id': 'oisoCXKuSNC722b_RnI78w',
                    'type': 'distributed',
                    'label': 'Carga distribuída',
                    'position': {
                        'value': force_distributed_pos,
                        'display': '1',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'magnitude': {
                        'value': force_distributed_mod,
                        'display': '-47.7',
                        'units': 'N/m',
                        'unitsKey': 'newton-per-meter',
                    },
                    'position2': {
                        'value': force_distributed_pos2,
                        'display': '0.3',
                        'units': 'm',
                        'unitsKey': 'meter',
                    },
                    'magnitude2': {
                        'value': force_distributed_mod2,
                        'display': '-47.7',
                        'units': 'N/m',
                        'unitsKey': 'newton-per-meter',
                    },
                    'iconSvg': '<svg xmlns:svg=\'http://www.w3.org/2000/svg\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 44 44\' class=\'j_WRkA\'><style>.eRimDg{stroke:rgba(112,150,182,1);stroke-width:2}.j_WRkA{fill:none;stroke-linecap:round;stroke-linejoin:round}</style><path d=\'M10.6,29.6L10.6,13.4 M7.6,24.7L10.6,29.6L13.5,24.7 M18.2,29.6L18.2,13.4 M15.3,24.7L18.2,29.6L21.1,24.7 M25.8,29.6L25.8,13.4 M22.9,24.7L25.8,29.6L28.7,24.7 M33.4,29.6L33.4,13.4 M30.5,24.7L33.4,29.6L36.4,24.7 M10.6,13.4L18.2,13.4L25.8,13.4L33.4,13.4\' class=\'eRimDg load _\'/></svg>',
                },
            ]

def do_put():

        force1_position = p1.get()
        force1_mod = f1.get()
        moment_position = p1.get()
        moment_value = m1.get()
        force2_position = p2.get()
        force2_mod = f2.get()
        force_distributed_pos = p3.get()
        force_distributed_mod = co.get()
        force_distributed_pos2 = p4.get()
        force_distributed_mod2 = co.get()


        
        var_list = [0.3, -41.79, 1.55626, 0.6, -51.2, 0.16, -44.5, 0.440, -44.5]

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-DE,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,de-DE;q=0.6,de;q=0.5,en-US;q=0.4',
            'Connection': 'keep-alive',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            'Origin': 'https://deflection.app',
            'Referer': 'https://deflection.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'language': 'pt',
        }


        json_data = {
            'updatedOn': '2022-11-11T23:56:13Z',
            'beamLength': {
                'value': 0.6,
                'display': '0.6',
                'units': 'm',
                'unitsKey': 'meter',
            },
            'deflectionLimitDenominator': 360,
            'materialName': '',
            'elasticModulus': {
                'value': 73,
                'display': '73',
                'units': 'GPa',
                'unitsKey': 'gigapascal',
            },
            'weightDensity': {
                'value': 76982.2025,
                'display': '77×10³',
                'units': 'N/m³',
                'unitsKey': 'newton-per-cubic-meter',
            },
            'bendingStrength': {
                'value': 248211262.554061,
                'display': '248×10⁶',
                'units': 'Pa',
                'unitsKey': 'pascal',
            },
            'shearStrength': {
                'value': 143217898.493693,
                'display': '143×10⁶',
                'units': 'Pa',
                'unitsKey': 'pascal',
            },
            'yieldStrength': {
                'value': 248211262.554061,
                'display': '248×10⁶',
                'units': 'Pa',
                'unitsKey': 'pascal',
            },
            'crossSectionDesignation': '',
            'area': {
                'value': 114,
                'display': '114',
                'units': 'cm²',
                'unitsKey': 'centimeter-squared',
            },
            'momentOfInertia': {
                'value': 0.0257,
                'display': '25.7×10⁻³',
                'units': 'm⁴',
                'unitsKey': 'meter-fourth',
            },
            'applyBeamWeight': False,
            'loads': get_loads(force1_position, force1_mod,  moment_position, moment_value, force2_position, force2_mod, force_distributed_pos, force_distributed_mod, force_distributed_pos2, force_distributed_mod2)
        }

        
        print(p1.get(), p2.get(), p3.get(), p4.get(), f1.get(), f2.get(), co.get(), m1.get())
        
        response = requests.put('https://api-2.deflection.ketchep.com/design/ejliCAfITveyzlGciAAsPg', params=params, headers=headers, json=json_data)
        dado = json.loads(response.text)['results']['spans']
        print(dado)
        
        def get_max_value(dado):
            global lista_defl
            lista_defl = list()
            for elemento in dado:
                lista_defl.append(float(elemento['displacementMax']['value']))
            return print (max(lista_defl)),
        get_max_value(dado)    

        lb1['text'] = 'A deflexão máxima na viga é de {:.2f} mm'.format(max(lista_defl)*1000)


var_list = [0.3, -41.79, 1.55626, 0.6, -51.2, 0.16, -44.5, 0.440, -44.5]



# 5) Viga Curva:

# E -> Módulo de elasticidade do material
# Rc-> Raio de curvatura 
# I -> Momento de inércia
# esp -> Espessura
# larg -> Largura
# m_sup -> Massa do suporte
# m_anilha_1 -> Massa da anilha 1
# m_anilha_2 -> Massa da anilha 2
# m_anilha_3 -> Massa da anilha 3
# deform -> Deformação


def deformação_viga_curva():

    #Tútulo:

    Label(janela, text = 'VIGA CURVA:',fg = 'black',bg='orange').place(x=510,y=645)

    # Dados:
    
    m_anilha_1 = 3.02
    m_anilha_2 = 4.64
    m_anilha_3 = 7.64
    larg = 31.75*pow(10,-3)
    esp = 3.175*pow(10,-3)
    Rc = 367.5*pow(10,-3)
    E = 200*pow(10,9)
    I = 84.68*pow(10,-12)
    m_sup = 0.86

    # Dados de entrada (interface):

    Label(janela, text = 'Insira a massa total em Kgs (com exceção do suporte):', anchor = W).place(x=510,y=675)
    massa_anilhas = Entry(janela)
    massa_anilhas.place(x=510,y=695)

    lb = Label(janela, text="Resultado:")
    lb.place(x=510, y=755)

    def bt_onclick():
        
        carga_total = (float(massa_anilhas.get())+m_sup)*10
        deform = (float(carga_total)*pow(Rc,3)/(2*E*I))*1000

       
        lb["text"] ='A deflexão teórica de acordo com o teorema de castigliano \né de {:.2f} mm.'.format(float(deform))
    
    # Botão "Ok":
    
    bt = Button(janela, text='Ok', command = bt_onclick)
    bt.place(x=510,y=725)


# 6) Guindaste de torre:

# massa_carga -> Massa de carga
# lanca_guindaste -> Comprimento da lança guindaste
# dist_torre_cabo -> Distância entre torre e cabo 
# angulo_torre_cabo -> Ângulo entre torre e cabo
# f -> força F

# Equação de momento:

def guindaste_de_torre():

    #Tútulo:

    Label(janela, text = 'GUINDASTE DE TORRE:',fg = 'black',bg='purple').place(x=900,y=20)

   # Dados de entrada (interface):

    Label(janela, text = 'Insira a massa em Kg na extremidade da lança:', anchor = W).place(x=900,y=50)
    massa_carga = Entry(janela)
    massa_carga.place(x=900,y=70)
    Label(janela, text = 'Insira em módulo a posição em relação à torre do contrapeso em metros (caso não haja, insira 0):', anchor = W).place(x=900,y=100)
    x_cp = Entry(janela)
    x_cp.place(x=900,y=120)
    Label(janela, text = 'Insira o contrapeso em Kg(caso não haja, insira 0):', anchor = W).place(x=900,y=150)
    cp = Entry(janela)
    cp.place(x=900,y=170)
    lanca_guindaste = 1.95
    dist_torre_cabo = 1.00
    angulo_torre_cabo = 30
    lb = Label(janela, text="Resultado:")
    lb.place(x=900, y=230)

    # Resultado de saída:
    
    def bt_onclick():
        f = ((float(massa_carga.get())*9.81*1.95)-(float(x_cp.get())*float(cp.get())))/(math.sin(math.radians(angulo_torre_cabo))*dist_torre_cabo)
        lb["text"] = 'A carga teórica é de {:.2f} N\nA tensão no cabo é de {:.2f} N'.format(float(f),float(f)/math.sin(math.radians(30)))     

    # Botão "Ok":
   
    bt = Button(janela, text='Ok', command = bt_onclick)
    bt.place(x=900,y=200)

guindaste_de_torre()
deformação_viga_curva()
deflexao_viga_hiperestatica()
tensões_e_deformações_tubo()
deflexao_trelica_plana()
vaso_de_pressão()

#Fechamento da janela:    

janela.mainloop()

