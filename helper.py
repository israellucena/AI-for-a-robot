#Funções Auxiliadoras

#Bibliotecas
import csv
import math
import networkx as nx
import sys

#Função que indica se o nome recebido é feminino
def feminino(nome):
	#Verificando no primeiro arquivo csv
	with open('nomesfemininos.csv', 'r', encoding='ISO-8859-1') as csvFile:
		csvReader = csv.reader(csvFile)
		for row in csvReader:
			if(row[1] == nome):
				return True
				
	#Verificando no segundo arquivo csv
	with open('nomesfemininos2.csv', 'r') as csvFile2:
		csvReader2 = csv.reader(csvFile2)
		for row in csvReader2:
			if(row[0] == nome):
				return True
	return False
    
#Função que indica se os dois pontos recebidos possuem ao menos uma distância de 110 unidades
def distancia_suficiente(ponto1, ponto2):
	#Utiliza-se uma fórmula para descobrir a distância entre dois pontos de R²
	if(math.sqrt(((ponto1[0]-ponto2[0])**2)+((ponto1[1]-ponto2[1])**2)) >= 110):
		return True
	return False

#Função que retorna a distância entre dois pontos de R²
def distancia(ponto1, ponto2):
	#Utiliza-se uma fórmula para descobrir a distância entre dois pontos de R²
	return math.sqrt(((ponto1[0]-ponto2[0])**2)+((ponto1[1]-ponto2[1])**2))

#Função que indica a zona em que o robô se encontra. Ps: "zona" - zona em que o robô se
#encontra. "c" - campo de pesquisa.
def zona(posicao, G):
	#Definindo o campo de pesquisa (Para simplificar a pesquisa)
	#Se o robô estiver entre as zonas 7,8,9,10 e 11
	if(posicao[1] <= 150):
		c = [7,8,9,10,11]
	#Se o robô estiver entre as zonas 1,2,3,4,5 e 6
	elif(posicao[1] <= 449):
		c = [1,2,3,4,5,6]
	#Se o robô estiver entre as zonas 12,13,14,15 e 16
	else:
		c = [12,13,14,15,16]
		
	#Pesquisa
	for i in c:
		if(posicao[0] >= G.nodes[i]["x1"] and posicao[0] <= G.nodes[i]["x2"] and posicao[1] >= G.nodes[i]["y1"] and posicao[1] <= G.nodes[i]["y2"]):
			zona_num = i
			zona_nome = G.nodes[i]["desig"]
			break

	return zona_num,zona_nome

#Função que atualiza os atributos "desig", "adulto", "crianca" ou "carrinho" da zona atual do
#robô. Ps: "c" - campo de pesquisa. "atributo" - inteiro que indica o atributo a alterar, sendo
#eles os seguintes: 1 - desig, 2 - adulto, 3 - crianca, 4 - carrinho. "zona" - designação da
#zona, para o caso do atributo ser igual a 1.
def atualiza_atributo(posicao, G, atributo, zona):
	#Definindo o campo de pesquisa (Para simplificar a pesquisa)
	#Se o robô estiver entre as zonas 7,8,9,10 e 11
	if(posicao[1] <= 150):
		c = [7,8,9,10,11]
	#Se o robô estiver entre as zonas 1,2,3,4,5 e 6
	elif(posicao[1] <= 449):
		c = [1,2,3,4,5,6]
	#Se o robô estiver entre as zonas 12,13,14,15 e 16
	else:
		c = [12,13,14,15,16]
		
	#Pesquisa
	for i in c:
		#Se encontrou a zona atual
		if(posicao[0] >= G.nodes[i]["x1"] and posicao[0] <= G.nodes[i]["x2"] and posicao[1] >= G.nodes[i]["y1"] and posicao[1] <= G.nodes[i]["y2"]):
			if(atributo == 1):
				G.nodes[i]["desig"] = zona
			elif(atributo == 2):
				G.nodes[i]["adulto"] = True
			elif(atributo == 3):
				G.nodes[i]["crianca"] = True
			elif(atributo == 4):
				G.nodes[i]["carrinho"] = True
			break
			
	return G
	
#Função que indica o número da zona correspondente à string recebida
def zona_pesquisa(G, nome_zona):
	for i in range(1,17):
		if(G.nodes[i]["desig"] == nome_zona):
			return i
	#Se o robô não conhece nenhum caminho para a zona "nome_zona"
	return -1
	
#Pesquisa o menor caminho (e sua distância) entre um ponto do supermercado e uma zona
#A função retorna a lista do menor caminho a ser seguido e o custo da distância (a partir da 
#posição atual). Ps: "caminho_list" (Inicialmente []) - Lista do caminho a ser seguido.
#"visitados_list" (Inicialmente []) - Lista de nodos visitados
def Pesquisa_Caminho(partida, destino, G, posicao, caminho_list, visitados_list):	
	#Custo final a ser retornado
	custo = sys.maxsize
	#Custo da posição atual até a fronteira
	custo_front = 0
	#Auxiliares
	custo_aux = 0 #Custo a partir do nodo atual da pesquisa
	caminho_list_aux = [] #Caminho a partir do nodo atual
	#Cópias
	visitados_list_copia = visitados_list.copy() #Lista de nodos visitados enviado como argumento
	visitados_list_copia.append(partida)
	caminho_list_copia = caminho_list.copy() #Cópia da lista "caminho_list"
	caminho_list_copia.append(partida)
	
	#Se a pesquisa chegou ao destino
	if(partida == destino):
		return 0, caminho_list_copia
	#Pesquisa, dentre todos, o caminhos possíveis, o menor deles
	for i in dict(nx.bfs_successors(G, source = partida, depth_limit = 1))[partida]:
		if i not in visitados_list:
			custo_front = distancia(posicao,G[partida][i]["front"]) #Calcula o custo até a fronteira
			custo_aux, caminho_list_aux = Pesquisa_Caminho(i, destino, G, G[partida][i]["front"], caminho_list_copia, visitados_list_copia)
			if(custo_aux + custo_front < custo):
				custo = custo_aux + custo_front
				caminho_list = caminho_list_aux.copy()

	return custo, caminho_list
	
#Estima o tempo decorrido do programa quando o nível da bateria do robô for igual a
#"nivel_bateria_estimar"
def calcular_regressao(nivel_bateria_estimar, nivel_bateria_regressao_linear):
	#Número de casas
	N = len(nivel_bateria_regressao_linear)
	#Soma de (xiyi)
	S_xy = 0
	#Soma de (xi)
	S_x = 0
	#Soma de (yi)
	S_y = 0
	#Soma de (xi²)
	S_x2 = 0
	
	for i in nivel_bateria_regressao_linear:
		#Soma de (xiyi)
		S_xy += i[0] * i[1]
		#Soma de (xi)
		S_x += i[0]
		#Soma de (yi)
		S_y += i[1]
		#Soma de (xi²)
		S_x2 += i[0]**2
		
	#(Soma de (xi))²
	S_x_2 = S_x**2
	
	#Calculando o w1 e o w0
	w1 = ((N*S_xy) - (S_x*S_y))/((N*S_x2) - (S_x_2))
	w0 = (S_y - (w1*S_x))/N
	
	#Retorna o tempo estimado
	return (w1*nivel_bateria_estimar)+w0

#Retorna a probabilidade (float) de encontrar um adulto numa zona se lá estiver uma criança,
#mas não estiver um carrinho
def calcular_probabilidade_resp8(G):
	#Probabilidade final -> P(A|Cr,~C)
	P_Final = 0.0
	#Probabilidade P(A,Cr,~C)
	P_Numerador = 0.0
	#Probabilidade P(Cr,~C)
	P_Denominador = 0.0
	#Probabilidade P(~C)
	P_NaoCarrinho = 0.0
	#Probabilidade P(A^~C)
	P_Adulto_E_NaoCarrinho = 0.0
	#Probabilidade P(Cr^~C)
	P_Crianca_E_NaoCarrinho = 0.0
	
	#Pesquisa
	for i in range(1,17):
		if(G.nodes[i]["carrinho"] == False):
			P_NaoCarrinho += 1
		if(G.nodes[i]["adulto"] == True and G.nodes[i]["carrinho"] == False):
			P_Adulto_E_NaoCarrinho += 1
		if(G.nodes[i]["crianca"] == True and G.nodes[i]["carrinho"] == False):
			P_Crianca_E_NaoCarrinho += 1
	
	P_NaoCarrinho /= 16
	P_Adulto_E_NaoCarrinho /= 16
	P_Crianca_E_NaoCarrinho /= 16
	
	#Probabilidade final -> P(A|Cr,~C) = P(A,Cr,~C)/P(Cr,~C)
	#P(A,Cr,~C) = P(Cr|A,~C) * P(A|~C) * P(~C)
	#P(Cr,~C) = P(Cr|~C) * P(~C)
	#Ps: Segundo o enunciado, P(Cr|A,~C) = 0.5
	
	#Evitando divisões por zero
	if(P_NaoCarrinho == 0):
		return 0
	if(((P_Crianca_E_NaoCarrinho/P_NaoCarrinho)*(P_NaoCarrinho)) == 0):
		return 0
	
	P_Final = ((0.5)*(P_Adulto_E_NaoCarrinho/P_NaoCarrinho)*(P_NaoCarrinho))/((P_Crianca_E_NaoCarrinho/P_NaoCarrinho)*(P_NaoCarrinho))
	
	return P_Final
