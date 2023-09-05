"""
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
40715, Israel Torres
40752, Felipe Vilchez

"""

#Bibliotecas
import time
import helper
import networkx as nx

#Variáveis globais
#Ligadas ao robô
posicao_atual = [-1,-1] #Posição atual do robô
nivel_bateria_atual = -1 #Nível atual da bateria
nivel_bateria_regressao_linear = [[100,0]] # Lista para estimar o nível da bateria em função do
#tempo decorrido. Cada índice da lista é representado da seguinte forma: [x, y], onde "x" indica
#o nível da bateria e "y" indica o tempo decorrido (do programa) em segundos em que o nível da
#bateria se iguala a "x".  
tempo_inicial = time.time() #Tempo inicial do programa
tempo_atual = time.time() #Tempo atual do programa

#Rede de zonas do mapa
G = nx.Graph()
#Definindo a área e a designação de cada zona. Cada zona é representada da seguinte forma:
#(int, x1, x2, y1, y2, string, bool, bool, bool), onde "int" é o número da zona, "x1,x2,y1,y2"
#são os pontos da área (onde x1 > x2 e y1 > y2), "string" é a string que designa a zona
#(ex: Papelaria, Talho, etc), e os bools indicam, respectivamente, se na zona há algum adulto,
#alguma criança ou algum carrinho.
G.add_nodes_from([(1,{"x1":29, "x2":145, "y1":151, "y2":449, "desig":'Corredor 1', "adulto":False, "crianca":False, "carrinho":False}),
                  (2,{"x1":146, "x2":299, "y1":151, "y2":286, "desig":'Corredor 2', "adulto":False, "crianca":False, "carrinho":False}),
                  (3,{"x1":146, "x2":299, "y1":329, "y2":449, "desig":'Corredor 3', "adulto":False, "crianca":False, "carrinho":False}),
                  (4,{"x1":300, "x2":436, "y1":151, "y2":449, "desig":'Corredor 4', "adulto":False, "crianca":False, "carrinho":False}),
                  (5,{"x1":437, "x2":771, "y1":151, "y2":286, "desig":'Corredor 5', "adulto":False, "crianca":False, "carrinho":False}),
                  (6,{"x1":437, "x2":771, "y1":329, "y2":449, "desig":'Corredor 6', "adulto":False, "crianca":False, "carrinho":False}),
                  (7,{"x1":29, "x2":136, "y1":29, "y2":150, "desig":'Entrada (Zona 7)', "adulto":False, "crianca":False, "carrinho":False}),
                  (8,{"x1":179, "x2":286, "y1":29, "y2":150, "desig":'Zona 8', "adulto":False, "crianca":False, "carrinho":False}),
                  (9,{"x1":329, "x2":436, "y1":29, "y2":150, "desig":'Zona 9', "adulto":False, "crianca":False, "carrinho":False}),
                  (10,{"x1":479, "x2":586, "y1":29, "y2":150, "desig":'Zona 10', "adulto":False, "crianca":False, "carrinho":False}),
                  (11,{"x1":629, "x2":771, "y1":29, "y2":150, "desig":'Zona 11', "adulto":False, "crianca":False, "carrinho":False}),
                  (12,{"x1":629, "x2":771, "y1":450, "y2":571, "desig":'Zona 12', "adulto":False, "crianca":False, "carrinho":False}),
                  (13,{"x1":479, "x2":586, "y1":450, "y2":571, "desig":'Zona 13', "adulto":False, "crianca":False, "carrinho":False}),
                  (14,{"x1":329, "x2":436, "y1":450, "y2":571, "desig":'Zona 14', "adulto":False, "crianca":False, "carrinho":False}),
                  (15,{"x1":179, "x2":286, "y1":450, "y2":571, "desig":'Zona 15', "adulto":False, "crianca":False, "carrinho":False}),
                  (16,{"x1":29, "x2":136, "y1":450, "y2":571, "desig":'Zona 16', "adulto":False, "crianca":False, "carrinho":False})])
                  
#Adicionando as ligações entre as zonas. Ps: "front" designa a posição da fronteira
G.add_edges_from([(1,2,{"front":[145.5,225]}),
                  (1,7,{"front":[85,150.5]}),
                  (1,3,{"front":[145.5,380]}),
                  (1,16,{"front":[85,449.5]}),
                  (2,8,{"front":[235,150.5]}),
                  (2,4,{"front":[299.5,225]}),
                  (3,4,{"front":[299.5,380]}),
                  (3,15,{"front":[235,449.5]}),
                  (4,9,{"front":[380,150.5]}),
                  (4,5,{"front":[436.5,225]}),
                  (4,6,{"front":[436.5,380]}),
                  (4,14,{"front":[380,449.5]}),
                  (5,10,{"front":[530,150.5]}),
                  (5,11,{"front":[695,150.5]}),
                  (6,12,{"front":[695,449.5]}),
                  (6,13,{"front":[530,449.5]})])
                  
#Ligadas às pessoas do sexo feminino
pessoas_feminino_list = ['',''] #Lista das últimas duas pessoas do sexo feminino vistas pelo
#robô. (Ps: As pessoas podem ser vistas mais de uma vez, mas o algoritmo evita que elas sejam
#calculadas nos casos em que a visão ocorre estritamente em seguida)
posicao_anterior_pessoa_feminino = [-1,-1] #Posição do robô na visão da(s) última(s) pessoa(s)
#do sexo feminino

#Ligadas às crianças e adultos
criancas_num = 0 #Número de crianças vistas
ultima_crianca = '' #Nome da última criança vista
posicao_anterior_crianca = [-1,-1] #Posição do robô na visão da última criança
adultos_num = 0 #Número de adultos vistos
ultimo_adulto = '' #Nome do último adulto visto
posicao_anterior_adulto = [-1,-1] #Posição do robô na visão do último adulto

def work(posicao, bateria, objetos):
	################################################################
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string

    # podem achar o tempo atual usando, p.ex.
    # time.time()
    ################################################################
        
    #Variáveis Globais
    #Ligadas ao robô
    global posicao_atual; posicao_atual = posicao #Definindo a posição atual do robô
    global posicao_anterior_pessoa_feminino
    global nivel_bateria_atual; nivel_bateria_atual = bateria #Definindo o nível atual da bateria
    global tempo_inicial #Tempo inicial do programa
    global tempo_atual; tempo_atual = time.time() #Tempo atual do programa
    
    #Rede de zonas do mapa
    global G
    
    #Ligadas às pessoas do sexo feminino
    global pessoas_feminino_list
    
    #Ligadas às crianças e adultos
    global criancas_num
    global ultima_crianca
    global posicao_anterior_crianca
    global adultos_num
    global ultimo_adulto
    global posicao_anterior_adulto
    
    #Atualizando a lista "nivel_bateria_regressao_linear"
    #Cada nível da bateria corresponde a apenas um espaço na lista
    if(nivel_bateria_regressao_linear[-1][0] != int(bateria)):
        nivel_bateria_regressao_linear.append([int(bateria),(tempo_atual-tempo_inicial)])
    
    #Analisando os objetos atuais da lista "objetos"
    for elemento_lista in objetos:
        categoria_objeto_atual = elemento_lista.rpartition('_')[0] #Nome da categoria do objeto
        #atual (Ex: zona, adulto, etc)
        nome_objeto_atual = elemento_lista.partition('_')[2] #Nome do objeto atual (Ex: talho,
        #Cláudia, caixa1, etc)
        
        #Se o objeto for uma pessoa
        if(categoria_objeto_atual in ['adulto','criança','funcionário']):
			#Se a pessoa for do sexo feminino
            if(helper.feminino(nome_objeto_atual)):
                #Se a pessoa atual é igual (em categoria e nome) à última pessoa vista
                if(elemento_lista == pessoas_feminino_list[-1]):
                    #Se a posição em que as duas pessoas foram vistas é "suficientemente"
                    #distante para sondar que sejam pessoas diferentes
                    if(helper.distancia_suficiente(posicao, posicao_anterior_pessoa_feminino)):
                        #A pessoa é adicionada na lista "pessoas_feminino_list"
                        pessoas_feminino_list[0] = pessoas_feminino_list[1]
                        pessoas_feminino_list[1] = elemento_lista
                        #Define a posição em que o robô teve a última visão de uma pessoa
                        #do sexo feminino
                        posicao_anterior_pessoa_feminino = posicao
                #Se a pessoa atual não é igual (em categoria e nome) à última pessoa vista
                else:
                    #A pessoa é adicionada na lista "pessoas_feminino_list"
                    pessoas_feminino_list[0] = pessoas_feminino_list[1]
                    pessoas_feminino_list[1] = elemento_lista
                    #Define a posição em que o robô teve a última visão de uma pessoa do
                    #sexo feminino
                    posicao_anterior_pessoa_feminino = posicao
            
            #Se a pessoa for uma criança
            if(categoria_objeto_atual in ['criança']):
                #Atualiza os atributos da zona atual
                G = helper.atualiza_atributo(posicao, G, 3, '')
                #Se a criança atual é igual (em categoria e nome) à última criança vista
                if(elemento_lista == ultima_crianca):
                    #Se a posição em que as duas crianças foram vistas é "suficientemente"
                    #distante para sondar que sejam crianças diferentes
                    if(helper.distancia_suficiente(posicao, posicao_anterior_crianca)):
                        #Incrementa o número de crianças vistas
                        criancas_num += 1
                        #A criança é adicionada à variável "ultima_crianca"
                        ultima_crianca = elemento_lista
                        #Define a posição em que o robô teve a última visão de uma criança
                        posicao_anterior_crianca = posicao
                #Se a criança atual não é igual (em categoria e nome) à última criança vista
                else:
                    #Incrementa o número de crianças vistas
                    criancas_num += 1
                    #A criança é adicionada à variável "ultima_crianca"
                    ultima_crianca = elemento_lista
                    #Define a posição em que o robô teve a última visão de uma criança
                    posicao_anterior_crianca = posicao
                
            #Se a pessoa for um adulto
            if(categoria_objeto_atual in ['adulto','funcionário']):
                #Atualiza os atributos da zona atual
                G = helper.atualiza_atributo(posicao, G, 2, '')
                #Se o adulto atual é igual (em categoria e nome) ao último adulto visto
                if(elemento_lista == ultimo_adulto):
                    #Se a posição em que os dois adultos foram vistos é "suficientemente"
                    #distante para sondar que sejam adultos diferentes
                    if(helper.distancia_suficiente(posicao,posicao_anterior_adulto)):
                        #Incrementa o número de adultos vistos
                        adultos_num += 1
                        #O objeto é adicionado à variável "ultimo_adulto"
                        ultimo_adulto = elemento_lista
                        #Define a posição em que o robô teve a última visão de um adulto
                        posicao_anterior_adulto = posicao
                #Se o adulto atual não é igual (em categoria e nome) ao último adulto visto
                else:
                    #Incrementa o número de adultos vistos
                    adultos_num += 1
                    #O objeto é adicionado à variável "ultimo_adulto"
                    ultimo_adulto = elemento_lista
                    #Define a posição em que o robô teve a última visão de um adulto
                    posicao_anterior_adulto = posicao
                
        #Se o objeto for uma zona
        elif(categoria_objeto_atual == 'zona'):         
            #Atualiza a designação da zona atual
            G = helper.atualiza_atributo(posicao, G, 1, nome_objeto_atual)
            
        #Se o objeto for uma zona de caixas
        elif(categoria_objeto_atual == 'caixa'):
			#Atualiza a designação da zona atual
            G = helper.atualiza_atributo(posicao, G, 1, 'caixas')
            
        #Se o objeto for um carrinho
        elif(categoria_objeto_atual == 'carrinho'):
            #Atualiza os atributos da zona atual
            G = helper.atualiza_atributo(posicao, G, 4, '')
	
def resp1():
	global pessoas_feminino_list
	penultima_pessoa_feminino = pessoas_feminino_list[0] #Penúltima Pessoa do Sexo Feminino
			
	#Imprime a resposta
	#Se há uma penúltima pessoa do sexo feminino
	if(penultima_pessoa_feminino != ''):
		nome_penultima_pessoa_feminino = penultima_pessoa_feminino.partition('_')[2] #Nome da
		#penúltima pessoa do sexo feminino
		#Imprime a resposta
		print('A penúltima pessoa do sexo feminino que vi foi a:', nome_penultima_pessoa_feminino)
	#Se o robô só tiver visto uma pessoa do sexo feminino
	elif(pessoas_feminino_list[1] != ''):
		#Imprime a resposta
		print('Só vi uma pessoa do sexo feminino')
	#Se o robô não tiver visto nenhuma pessoa do sexo feminino
	else:
		#Imprime a resposta
		print('Não vi nenhuma pessoa do sexo feminino')

def resp2():
	zona_atual_num, zona_atual_nome = helper.zona(posicao_atual, G) #Zona atual do robô
	
	#Imprime a resposta
	print('Estou na seguinte zona:', zona_atual_nome)

def resp3():
	#Verifica a zona atual em que o robô se encontra
	zona_atual_num, zona_atual_nome = helper.zona(posicao_atual, G)
	#Verifica se o robô já está na papelaria
	if(zona_atual_nome == 'papelaria'):
		#Imprime a resposta
		print('Já estás na zona da papelaria')
	else:
		#Verifica qual é a zona da papelaria
		zona_papelaria_num = helper.zona_pesquisa(G, 'papelaria')
		if(zona_papelaria_num == -1):
			#Imprime a resposta
			print('Não conheço nenhum caminho para a papelaria')
		else:
			custo, caminho_papelaria = helper.Pesquisa_Caminho(zona_atual_num, zona_papelaria_num, G, posicao_atual, [], [])
			#Imprime a resposta
			print('O caminho para a papelaria é:', end = ' ');
			for i in caminho_papelaria:
				if(i == caminho_papelaria[-1]):
					print(G.nodes[i]["desig"])
				else:
					print(G.nodes[i]["desig"], end = ', ')

def resp4():
	#Verifica a zona atual em que o robô se encontra
	zona_atual_num, zona_atual_nome = helper.zona(posicao_atual, G)
	#Verifica se o robô já está no talho
	if(zona_atual_nome == 'talho'):
		#Imprime a resposta
		print('Já estás na zona talho')
	else:
		#Verifica qual é o número zona do talho
		zona_talho_num = helper.zona_pesquisa(G, 'talho')
		#Se o robô ainda não descobriu o caminho para o talho
		if(zona_talho_num == -1):
			#Imprime a resposta
			print('Não conheço nenhum caminho para o talho')
		else:
			custo, caminho_talho = helper.Pesquisa_Caminho(zona_atual_num, zona_talho_num, G, posicao_atual, [], [])
			#Imprime a resposta
			print('A distância até o talho é:', "%.2f"%custo, 'unidades');

def resp5():
	#Verifica a zona atual em que o robô se encontra
	zona_atual_num, zona_atual_nome = helper.zona(posicao_atual, G)
	#Verifica se o robô já está no caixa
	if(zona_atual_nome == 'caixas'):
		#Imprime a resposta
		print('Já estás na zona de caixas')
	else:
		#Verifica qual é o número de caixas
		zona_caixa_num = helper.zona_pesquisa(G, 'caixas')
		#Se o robô ainda não descobriu o caminho para os caixas
		if(zona_caixa_num == -1):
			#Imprime a resposta
			print('Não conheço nenhum caminho para os caixas')
		else:
			#Formula da velocidade média : Velocidade média = (delta)posição/(delta)tempo
			#Fórmula do tempo: Tempo = (delta)posição/Velocidade média
			#A velocidade média foi calculada manualmente, selecionando várias retas do plano, e percorrendo-as,
			#salvando as informações e calculando a fórmula anterior. Ps: O tempo foi dado em dado em
			#segundos, e a posição foi dada de acordo com as unidades do plano cartesiano (indeterminada)
			velocidade = 240 #Unidades por segundos
			custo, caminho_caixas = helper.Pesquisa_Caminho(zona_atual_num, zona_caixa_num, G, posicao_atual, [], [])
			#Calcula o tempo até chegar ao caixa
			tempo = custo/velocidade
			#Imprime a resposta
			print('O tempo estimado até chegar ao caixa é:', "%.2f"%tempo, 'segundos')

def resp6():
	#Como a descarga da bateria depende também da movimentação do robô, optou-se por fazer uma
	#estimação a partir da regressão linear
	
	global nivel_bateria_atual
	global nivel_bateria_regressao_linear
	
	#Metade do nível da bateria atual
	metade_nivel_bateria_atual = int(nivel_bateria_atual/2)
	#Tempo estimado
	tempo_esperado = helper.calcular_regressao(metade_nivel_bateria_atual, nivel_bateria_regressao_linear.copy())
	
	#Imprime a resposta
	print('Estimo que fiques com metade da bateria que tens agora em:', "%.2f"%(tempo_esperado-(tempo_atual-tempo_inicial)), 'segundos')

def resp7():
	global criancas_num #Número total de adultos vistos
	global adultos_num #Número total de adultos vistos
	
	#Calculando a probabilidade de que a próxima pessoa que o robô encontre seja uma criança
	if(criancas_num != 0 or adultos_num != 0):
		probabilidade = criancas_num/(criancas_num+adultos_num)
		probabilidade *= 100
	else:
		probabilidade = 0
	
	#Imprime a resposta
	print("%.2f"%probabilidade, end = '% \n')

def resp8():
    #Calcula a probabilidade de encontrar um adulto numa zona se lá estiver uma criança, mas
    #não estiver um carrinho
    probabilidade = helper.calcular_probabilidade_resp8(G)
    probabilidade *= 100
    
    #Imprime a resposta
    print("%.2f"%probabilidade, end = '% \n')
