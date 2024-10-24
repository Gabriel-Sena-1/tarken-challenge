import cv2
import numpy as np

def contar_pontos_e_colisoes(imagem_path, cor_branca, cor_vermelha, cor_azul):
    """
    Conta os pontos de cor branca e vermelha em uma imagem e analisa colisões com área azul.

    Args:
        imagem_path (str): Caminho para a imagem.
        cor_branca (tuple): Tupla com os valores HSV mínimo e máximo para a cor branca.
        cor_vermelha (tuple): Tupla com os valores HSV mínimo e máximo para a cor vermelha.
        cor_azul (tuple): Tupla com os valores HSV mínimo e máximo para a cor azul.

    Returns:
        tuple: Tupla com o número de pontos brancos, vermelhos e meteoros que colidem com o lago.
    """

    # Carregar a imagem
    img = cv2.imread(imagem_path)
    altura, largura = img.shape[:2]

    # Converter para HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Definir os limites de cor
    lower_white = np.array(cor_branca[0])
    upper_white = np.array(cor_branca[1])
    
    lower_red_light = np.array(cor_vermelha[0])
    upper_red_light = np.array(cor_vermelha[1])
    lower_red_dark = np.array(cor_vermelha[2])
    upper_red_dark = np.array(cor_vermelha[3])

    lower_blue = np.array(cor_azul[0])
    upper_blue = np.array(cor_azul[1])

    # Criar máscaras
    mask_branco = cv2.inRange(hsv, lower_white, upper_white)
    mask_vermelho_light = cv2.inRange(hsv, lower_red_light, upper_red_light)
    mask_vermelho_dark = cv2.inRange(hsv, lower_red_dark, upper_red_dark)
    mask_vermelho = cv2.bitwise_or(mask_vermelho_light, mask_vermelho_dark)
    mask_lago = cv2.inRange(hsv, lower_blue, upper_blue)

    # Criar imagem para visualização
    img_resultado = np.zeros_like(img)
    img_resultado[mask_branco > 0] = [255, 255, 255]  # Pontos brancos
    img_resultado[mask_vermelho > 0] = [0, 0, 255]    # Meteoros
    img_resultado[mask_lago > 0] = [255, 0, 0]        # Lago
    
    # Mostrar a imagem com os pontos e trajetórias
    cv2.imshow('Meteoros estrelas e lago', img_resultado)
    cv2.imshow('Estrelas', mask_branco)
    cv2.imshow('Meteoros', mask_vermelho)
    cv2.imshow('Lago', mask_lago)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return cv2.countNonZero(mask_branco), cv2.countNonZero(mask_vermelho)

# Definição dos ranges de cores
branco = ((0, 0, 200), (180, 30, 255))
vermelho = (
    (0, 100, 100), (10, 255, 255),
    (160, 100, 100), (180, 255, 255)
)
azul = ((100, 150, 200), (130, 255, 255))  # Azul puro até azul escuro

# Executar análise
imagem = 'meteor_challenge_01.png'
estrelas, meteoros = contar_pontos_e_colisoes(imagem, branco, vermelho, azul)

print("Estrelas:", estrelas)
print("Meteoros:", meteoros)