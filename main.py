import sys
import numpy as np
import skimage as ski
from os.path import splitext

# def inverter_matizes_v1(img_atalho:str, H:float|int, d:float|int):
#     ''' Recebe uma imagem colorida e dois parâmetros numéricos H e d e que devolva uma outra imagem
#     colorida com alguns valores de matiz da imagem de entrada invertidos.'''
#     H = resto(H, 360)

#     imagem_rgb = ski.io.imread(img_atalho)
#     imagem_hsv = ski.color.rgb2hsv(imagem_rgb)
#     matiz_numpy = imagem_hsv[:, :, 0]
#     lista_matizes = matiz_numpy.tolist()

#     linhas = len(lista_matizes)
#     colunas = len(lista_matizes[0])

#     a = resto(H - d, 360)
#     b = resto(H + d, 360)

#     if d == 180:
#         for i in range(linhas):
#             for j in range(colunas):
#                 h = hsv_para_graus(lista_matizes[i][j])
#                 lista_matizes[i][j] = graus_para_hsv(resto(h - 180, 360))
#     elif b > a:
#         for i in range(linhas):
#             for j in range(colunas):
#                 h = hsv_para_graus(lista_matizes[i][j])
#                 if h >= a and h <= b:
#                     lista_matizes[i][j] = graus_para_hsv(resto(h - 180, 360))
#     elif b < a:
#         for i in range(linhas):
#             for j in range(colunas):
#                 h = hsv_para_graus(lista_matizes[i][j])
#                 if (h >= 0 and h <= b) or (h >= a and h < 360):
#                     lista_matizes[i][j] = graus_para_hsv(resto(h - 180, 360))

#     nova_matriz_matiz = np.array(lista_matizes)
    
#     imagem_hsv_modificada = imagem_hsv.copy()
#     imagem_hsv_modificada[:, :, 0] = nova_matriz_matiz
#     imagem_rgb_final = ski.color.hsv2rgb(imagem_hsv_modificada)

#     imagem_salvar = (imagem_rgb_final * 255).astype(np.uint8)
#     nome_base, _ = splitext(img_atalho)
#     nome_saida = f"{nome_base}_H={H}_d={d}.jpg"
#     ski.io.imsave(nome_saida, imagem_salvar)

def inverter_matizes_v2(img_atalho:str, H:float|int, d:float|int):
    ''' Recebe uma imagem colorida e dois parâmetros numéricos H e d e que devolva uma outraimagem
    colorida com alguns valores de matiz da imagem de entrada invertidos.'''
    H = resto(H, 360)

    imagem_rgb = ski.io.imread(img_atalho)
    imagem_hsv = ski.color.rgb2hsv(imagem_rgb)
    
    matiz_graus = hsv_para_graus(imagem_hsv[:, :, 0]) # pega só a parte referente à matiz

    a = resto(H - d, 360)
    b = resto(H + d, 360)

    # A lógica é criar uma máscara antes para onde for True a alteração vai ocorrer

    if d == 180:
        mascara = np.ones_like(matiz_graus, dtype=bool) # Matriz cheia de True
    elif b >= a:
        mascara = (matiz_graus >= a) & (matiz_graus <= b) #type:ignore
    else: # b < a
        mascara = (matiz_graus >= a) | (matiz_graus <= b) #type:ignore

    matiz_graus[mascara] = resto(matiz_graus[mascara] - 180, 360) #type:ignore

    imagem_hsv_modificada = imagem_hsv.copy()
    imagem_hsv_modificada[:, :, 0] = graus_para_hsv(matiz_graus)
    
    imagem_rgb_final = ski.color.hsv2rgb(imagem_hsv_modificada)
    imagem_salvar = (imagem_rgb_final * 255).astype(np.uint8)
    
    nome_base, _ = splitext(img_atalho)
    ski.io.imsave(f"{nome_base}_H={H}_d={d}.jpg", imagem_salvar)

def resto(dividendo:float|int, divisor:float|int) -> float|int:
    return dividendo % divisor

def hsv_para_graus(valor_skimage:float|int) -> float|int:
    '''Converte a matiz do scikit-image (0 a 1) para graus (0 a 360).'''
    return valor_skimage * 360

def graus_para_hsv(graus: float | int) -> float | int:
    '''Converte graus (0 a 360) de volta para a matiz do scikit-image (0 a 1).'''
    return graus / 360

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Erro! Modo de uso: python main.py <nome_imagem> <valor_H> <valor_d>")
        sys.exit(1)

    img_atalho = sys.argv[1]
    H = float(sys.argv[2])
    d = float(sys.argv[3])

    if d > 180 or d < 0:
        print("Erro! O parâmetro d deve estar no intervalo [0, 180]")
        sys.exit(1)

    inverter_matizes_v2(img_atalho, H, d)