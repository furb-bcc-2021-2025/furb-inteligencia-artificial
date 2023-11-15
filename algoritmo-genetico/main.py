import math
import random

import matplotlib.pyplot as plt
import numpy as np


class Cidade:
    def __init__(self, identificador, x, y):
        self.identificador = identificador
        self.x = x
        self.y = y


class Cromossomo:
    def __init__(self, cidades, custo_total):
        self.cidades = cidades
        self.custo_total = custo_total


class MatrizDistancias:
    def __init__(self, cidades):
        self.distancias_entre_cidades = []
        self.__calcular_distancias(cidades)

    def __calcular_distancias(self, cidades):
        for cidade_origem in cidades:
            distancia_cidades = []
            for cidade_destino in cidades:
                distancia = self.calcular_distancia(cidade_origem, cidade_destino)
                distancia_cidades.append(distancia)
            self.distancias_entre_cidades.append(distancia_cidades)

    def calcular_distancia(self, cidade_origem, cidade_destino):
        return math.sqrt(
            math.pow(cidade_origem.x - cidade_destino.x, 2) + math.pow(cidade_origem.y - cidade_destino.y, 2)
        )

    def obter_distancia(self, cidade_origem, cidade_destino):
        return self.distancias_entre_cidades[cidade_origem.identificador][cidade_destino.identificador]


def gerar_cromossomos_iniciais(cidades, matriz_distancias):
    cromossomos = []

    for i in range(len(cidades)):
        cidades_ordem_aleatoria = random.sample(cidades, len(cidades))
        custo_total = calcular_custo_total(cidades_ordem_aleatoria, matriz_distancias)
        cromossomos.append(Cromossomo(cidades_ordem_aleatoria, custo_total))

    return cromossomos


def calcular_custo_total(cidades, matriz_distancias):
    cidades_com_inicio_no_fim = cidades.copy()
    cidades_com_inicio_no_fim.append(cidades[0])
    custo_total = 0

    for i in range(len(cidades)):
        cidade_origem = cidades_com_inicio_no_fim[i]
        cidade_destino = cidades_com_inicio_no_fim[i + 1]
        custo_total += matriz_distancias.obter_distancia(cidade_origem, cidade_destino)

    return custo_total


def gerar_roleta_de_selecao_de_pais():
    roleta = []
    roleta.extend([0] * 10)
    roleta.extend([1] * 9)
    roleta.extend([2] * 8)
    roleta.extend([3] * 7)
    roleta.extend([4] * 6)
    roleta.extend([5] * 5)
    roleta.extend([6] * 4)
    roleta.extend([7] * 3)
    roleta.extend([8] * 2)
    roleta.extend([9] * 1)
    return roleta


def sortear_pares_de_pais(roleta):
    pares = []

    for i in range(5):
        pais_sorteados = random.choices(roleta, k=2)
        pares.append((pais_sorteados[0], pais_sorteados[1]))

    return pares


def cruzar_pares_de_pais(pares_de_pais, cromossomos, matriz_distancias):
    filhos = []

    for (ix_pai_1, ix_pai_2) in pares_de_pais:
        pai_1 = cromossomos[ix_pai_1]
        pai_2 = cromossomos[ix_pai_2]

        cidades_filho_1 = pai_1.cidades.copy()
        cidades_filho_2 = pai_2.cidades.copy()
        indice_troca = random.randrange(len(pai_1.cidades))

        trocar_cidades_entre_filhos(cidades_filho_1, cidades_filho_2, indice_troca)

        while True:
            (tem_duplicados, indice_duplicado) = verificar_cidades_duplicadas_filhos(cidades_filho_1, cidades_filho_2, indice_troca)

            if tem_duplicados:
                trocar_cidades_entre_filhos(cidades_filho_1, cidades_filho_2, indice_duplicado)
                indice_troca = indice_duplicado
            else:
                break

        filhos.append(Cromossomo(cidades_filho_1, calcular_custo_total(cidades_filho_1, matriz_distancias)))
        filhos.append(Cromossomo(cidades_filho_2, calcular_custo_total(cidades_filho_2, matriz_distancias)))

    return filhos


def trocar_cidades_entre_filhos(cidades_filho_1, cidades_filho_2, indice):
    cidade_filho_1_temp = cidades_filho_1[indice]
    cidade_filho_2_temp = cidades_filho_2[indice]

    cidades_filho_1[indice] = cidade_filho_2_temp
    cidades_filho_2[indice] = cidade_filho_1_temp
    return


def verificar_cidades_duplicadas_filhos(cidades_filho_1, cidades_filho_2, indice_troca):
    for i in range(len(cidades_filho_1)):
        filho_1_tem_duplicados = cidades_filho_1[i] == cidades_filho_1[indice_troca]
        filho_2_tem_duplicados = cidades_filho_2[i] == cidades_filho_2[indice_troca]

        if (filho_1_tem_duplicados or filho_2_tem_duplicados) and i != indice_troca:
            return True, i

    return False, -1


def realizar_mutacao_filhos(filhos):
    for filho in filhos:
        cidades_sorteadas = random.choices(range(len(filho.cidades)), k=2)

        cidade_1_temp = filho.cidades[cidades_sorteadas[0]]
        cidade_2_temp = filho.cidades[cidades_sorteadas[1]]

        filho.cidades[cidades_sorteadas[0]] = cidade_2_temp
        filho.cidades[cidades_sorteadas[1]] = cidade_1_temp

    return filhos


def ordenar_cromossomos_pelo_custo_total(cromossomos):
    return sorted(cromossomos, key=lambda cromossomo: cromossomo.custo_total)  # crescente


def exibir_cromossomos(cromossomos):
    for i in range(len(cromossomos)):
        cromossomo = cromossomos[i]
        print(f'#{str(i+1).zfill(2)} cromossomo - cidades: {[c.identificador for c in cromossomo.cidades]} - custo total: {cromossomo.custo_total}')


def exibir_cidades_interligadas_pelo_melhor_caminho(cidades, cidades_melhor_caminho):
    eixo_x = [cidade.x for cidade in cidades]
    eixo_y = [cidade.y for cidade in cidades]

    melhor_caminho_x = [cidade.x for cidade in cidades_melhor_caminho]
    melhor_caminho_y = [cidade.y for cidade in cidades_melhor_caminho]

    plt.plot(eixo_x, eixo_y, marker='o', color='r', ls='')
    plt.plot(melhor_caminho_x, melhor_caminho_y)
    plt.xlabel('eixo x')
    plt.ylabel('eixo y')
    plt.title('Coordenadas das cidades interligadas pelo melhor caminho encontrado')
    plt.show()


if __name__ == '__main__':
    print('\nInicio da execução\n')

    # carregar dados do enunciado
    data = np.loadtxt('cidades.mat')

    # gerar objetos de cidade
    cidades = [Cidade(i, data[0][i], data[1][i]) for i in range(20)]

    # gerar matriz de distancias entre cidades
    matriz_distancias = MatrizDistancias(cidades)

    # gerar cromossomos iniciais
    cromossomos_iniciais = gerar_cromossomos_iniciais(cidades, matriz_distancias)
    cromossomos = cromossomos_iniciais.copy()

    # executar 10000 vezes
    for i in range(10000):

        if i % 1000 == 0:
            print(f'- Executando {str(i)} gerações')

        # ordenar cromossomos pelo custo total
        cromossomos = ordenar_cromossomos_pelo_custo_total(cromossomos)

        # eliminar os 10 piores cromossomos
        cromossomos = cromossomos[:len(cromossomos) // 2]

        # gerar roleta de selecao de pais para cruzamento
        roleta = gerar_roleta_de_selecao_de_pais()

        # sortear pares de pais para cruzamento
        pares_de_pais = sortear_pares_de_pais(roleta)

        # cruzar pares de pais selecionados
        filhos = cruzar_pares_de_pais(pares_de_pais, cromossomos, matriz_distancias)

        # realizar mutacao dos genes dos filhos gerados
        filhos = realizar_mutacao_filhos(filhos)

        # inserir filhos na lista de cromossomos
        cromossomos.extend(filhos)

    print('\nFim da execução')

    print('\nResultados')

    print(f'\nPopulação inicial - tamanho: {len(cromossomos_iniciais)}\n')

    cromossomos_iniciais = ordenar_cromossomos_pelo_custo_total(cromossomos_iniciais)
    exibir_cromossomos(cromossomos_iniciais)

    print(f'\nPopulação final - tamanho: {len(cromossomos)}\n')

    cromossomos = ordenar_cromossomos_pelo_custo_total(cromossomos)
    exibir_cromossomos(cromossomos)

    exibir_cidades_interligadas_pelo_melhor_caminho(cidades, cromossomos[0].cidades)

