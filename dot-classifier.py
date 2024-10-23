import cv2
import numpy as np

def contar_pontos_por_cor(imagem_path, cor_branca, cor_vermelha):
    """
    Conta os pontos de cor branca e vermelha em uma imagem.

    Args:
        imagem_path (str): Caminho para a imagem.
        cor_branca (tuple): Tupla com os valores HSV mínimo e máximo para a cor branca.
        cor_vermelha (tuple): Tupla com os valores HSV mínimo e máximo para a cor vermelha.

    Returns:
        tuple: Tupla com o número de pontos brancos e vermelhos, respectivamente.
    """

    # Carregar a imagem
    img = cv2.imread(imagem_path)

    # Converter para HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Definir os limites de cor
    lower_white = np.array(cor_branca[0])
    upper_white = np.array(cor_branca[1])
    
    # Limites para a cor vermelha (incluindo dois intervalos)
    lower_red_light = np.array(cor_vermelha[0])
    upper_red_light = np.array(cor_vermelha[1])
    
    lower_red_dark = np.array(cor_vermelha[2])
    upper_red_dark = np.array(cor_vermelha[3])

    # Criar máscaras
    mask_branco = cv2.inRange(hsv, lower_white, upper_white)
    mask_vermelho_light = cv2.inRange(hsv, lower_red_light, upper_red_light)
    mask_vermelho_dark = cv2.inRange(hsv, lower_red_dark, upper_red_dark)

    # Combinar as máscaras vermelhas
    mask_vermelho = cv2.bitwise_or(mask_vermelho_light, mask_vermelho_dark)

    # Criar uma imagem colorida para visualização
    img_resultado = np.zeros_like(img)
    img_resultado[mask_branco > 0] = [255, 255, 255]  # Pontos brancos em branco
    img_resultado[mask_vermelho > 0] = [0, 0, 255]    # Pontos vermelhos em vermelho

    # Mostrar a imagem com os pontos
    cv2.imshow('Pontos Detectados', img_resultado)
    cv2.imshow('Mascara de brancos', mask_branco)
    cv2.imshow('Mascara de vermelhos', mask_vermelho)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Contar os pontos
    pontos_brancos = cv2.countNonZero(mask_branco)
    pontos_vermelhos = cv2.countNonZero(mask_vermelho)

    return pontos_brancos, pontos_vermelhos

# Exemplo de uso
imagem = 'meteor_challenge_01.png'  # Substitua pelo caminho da sua imagem

# Ajuste os valores HSV para a cor branca
branco = ((0, 0, 200), (180, 30, 255))

# Ajuste os valores HSV para a cor vermelha
vermelho = (
    (0, 100, 100), (10, 255, 255),    # Vermelho próximo a 0 graus
    (160, 100, 100), (180, 255, 255)  # Vermelho próximo a 180 graus
)

resultado = contar_pontos_por_cor(imagem, branco, vermelho)

print("Pontos brancos:", resultado[0])
print("Pontos vermelhos:", resultado[1])