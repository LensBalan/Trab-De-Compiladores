import pandas as pd

# Autores: Leonardo Balan e Gabriel Santos da Silva

# Analisador Lexico - Compiladores
#Linguagem de Programaçao: GLprog

#Inicio


#------------------------------------- Lexico -------------------------------------------

#Lista para armazenar a tabela de Tokens(Token, Lexema)
tabela_de_tokens = []

#Automato de Reconhecimento
#Estados e transicoes do automato
def transicao(estado, caracter):
    if estado == 'e1': 
        if 'A' <= caracter <= 'Z':
          return 'e2'
        if '0' <= caracter <= '9':
          return 'e11'
        if 'a' <= caracter <= 'z':
          return 'e4'
        if caracter == '!':
          return 'e6'
        if caracter == ' ' or caracter == '\n':
          return 'e9'
        if caracter == '(':
          return 'e16'
        if caracter == ')':
          return 'e17'
        if caracter == '.':
          return 'e18'
        if caracter in '+-*/': # '+' ou '-' ou '*' ou '/'
          return 'e19'
        if caracter in '><':
          return 'e20'
        if caracter == '^':
          return 'e21'
        if caracter == '{':
          return 'e27'
        if caracter == '}':
          return 'e28'
        return 'e10'  # Qualquer outro caracter vai para o estado e10 (erro)
    elif estado == 'e2': 
        if 'A' <= caracter <= 'Z': 
          return 'e2'
        if caracter == ' ' or caracter == '\n':
          return 'e3'
        return 'e25' # Erro, ID invalido
    elif estado == 'e4':
        if '0' <= caracter <= '9':
          return 'e4'
        if 'a' <= caracter <= 'z':
          return 'e4'
        if caracter == ' ' or caracter == '\n':
          return 'e5'
        return 'e26' # Erro, nome_var invalido'
    elif estado == 'e6':
        if caracter == '!':
          return 'e7'
        return 'e10'
    elif estado == 'e7':
        if 'a' <= caracter <= 'z':
          return 'e7'
        if 'A' <= caracter <= 'Z':
          return 'e7'
        if '0' <= caracter <= '9':
          return 'e7'
        if caracter == ' ':
          return 'e7'
        if caracter == '\n':
          return 'e8'
    elif estado == 'e11':
        if '0' <= caracter <= '9':
          return 'e11'
        if caracter == ',':
          return 'e13'
        if caracter == ' ' or caracter == '\n':
          return 'e12'
        return 'e24' #Erro, numero invalido
    elif estado == 'e13':
        if '0' <= caracter <= '9':
          return 'e14' 
        return 'e24' #Erro, numero invalido
    elif estado == 'e14':
        if '0' <= caracter <= '9':
          return 'e14'
        if caracter == ' ' or caracter == '\n':
          return 'e15'
        return 'e24' #Erro, numero invalido
    elif estado == 'e21':
      if caracter != '^':
        return 'e22'
      if caracter == '^':
        return 'e23'
    elif estado == 'e22':
        if caracter != '^':
          return 'e22'
        if caracter == '^':
          return 'e23'

# Estado Inicial
estado_inicial = 'e1'
#Estado de erro
estado_erro = 'e10'
# Estados de Aceitacao (reconhecimento)
estado_final = {
    'e3': 'ID',
    'e5': 'Variavel',
    'e8': 'Comentario',
    'e9': 'Espaco',
    'e10': 'ERRO, caracter_invalido',
    'e12': 'Num_inteiro',
    'e15': 'Num_real',
    'e16': '(',
    'e17': ')',
    'e18': '.',
    'e19': 'op_arit',
    'e20': 'op_relacional',
    'e23': 'Caracter',
    'e24': 'ERRO, numero_invalido',
    'e25': 'ERRO, ID_invalido',
    'e26': 'ERRO, nome_var_invalido',
    'e27': '{',
    'e28': '}'
}

# Modifica a função processar_codigo para evitar salvar comentários e espaços
def processar_codigo(codigo):
    estado = estado_inicial  # estado de inicio de exec
    lexema = ''  # var para armazenar o lexema
    linha = 1  # var para armazenar a linha atual

    with open(codigo, 'r') as codigo:  # Ler o arq
        while True:
            caracter = codigo.read(1)  # Lendo caractere por caractere
            if not caracter:
                if lexema:
                    # Processa o último lexema ao final do arquivo
                    if estado in estado_final:
                        token = estado_final[estado]
                        if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                            tabela_de_tokens.append((token, lexema.strip(), linha))
                    else:
                        tabela_de_tokens.append(('ERRO, Caracter Invalido', lexema.strip(), linha))
                break

            # Incrementa a linha se encontrar nova linha
            if caracter == '\n':
                linha += 1

            novo_estado = transicao(estado, caracter)

            if novo_estado:
                if novo_estado == estado_erro:
                    if lexema:
                        # Adiciona o token acumulado até o erro
                        if estado in estado_final:
                            token = estado_final[estado]
                            if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                                tabela_de_tokens.append((token, lexema.strip(), linha))
                        else:
                            tabela_de_tokens.append(('ERRO, caracter invalido', lexema.strip(), linha))

                    # Adiciona o caractere atual como erro
                    tabela_de_tokens.append(('ERRO, caracter invalido', caracter, linha))

                    # Reinicia o estado
                    estado = estado_inicial
                    lexema = ''

                elif novo_estado in estado_final:
                    lexema += caracter  # Adiciona o caractere ao lexema
                    token = estado_final[novo_estado]
                    if token not in {'Comentario', 'Espaco'}:  # Ignora comentário e espaço
                        tabela_de_tokens.append((token, lexema.strip(), linha))

                    # Reinicia o estado
                    estado = estado_inicial
                    lexema = ''
                else:
                    estado = novo_estado
                    lexema += caracter  # Adiciona caractere ao lexema

            else:
                # Estado inválido, trata o lexema atual como erro
                if lexema:
                    if estado in estado_final:
                        token = estado_final[estado]
                        tabela_de_tokens.append((token, lexema.strip(), linha))
                    else:
                        tabela_de_tokens.append(('ERRO', lexema.strip(), linha))

                # Adiciona o caractere atual como erro
                tabela_de_tokens.append(('ERRO', caracter, linha))

                # Reinicia o estado
                estado = estado_inicial
                lexema = ''

processar_codigo('codigo.txt')

#print ("Tabela de Tokens (Token, Lexema):\n")
#for token in tabela_de_tokens:
  #print(token)

#Dic para obter_token()
Tipos_id = {
    'SE': 'SE',
    'SENAO': 'SENAO',
    'DURANTE': 'DURANTE',
    'PARA': 'PARA',
    'INTEIRO': 'INTEIRO',
    'REAL': 'REAL',
    'CARACTER': 'CARACTER',
    'ZEROUM': 'ZEROUM',
    'AND': 'Op_logico',
    'OR': 'Op_logico',
    'RECEBA': 'RECEBA',
    'RECEBAT': 'RECEBAT',
    'ESCREVA': 'ESCREVA',
    'INICIO': 'INICIO',
    'FIM': 'FIM',
    'INC': 'INC',
    'DIF': 'op_relacional',
    'IGUAL': 'op_relacional',
}

# Func para obter o token correto pros ID
def obter_token(lexema):
    return Tipos_id.get(lexema, 'ID')

# Lista para armazenar os tokens atualizados
tokens_atualizados = []

# Substitui 'ID' pelo token correto com base no lexema
for token, lexema, linha in tabela_de_tokens:
    if token == 'ID':
        novo_token = obter_token(lexema)
        tokens_atualizados.append((novo_token, lexema, linha))
    else:
        tokens_atualizados.append((token, lexema, linha))

print("\n Tabela de Tokens: \n")
for token in tokens_atualizados:
    print(token[0])

print()

# ------------------------------- Sintático ---------------------------------------

def carregar_tabela_SLR(arq):
    #Carrega a planilha
    tabela = pd.read_excel(arq, index_col=0)  # index_col=0 define a primeira coluna como os estados
    return tabela

# arq excel
arq = 'Tabela_SLR3.xlsx'
tabela_SLR = carregar_tabela_SLR(arq)
print("Tabela SLR Carregada.")
print()

#Interpretar E, R, AC e desvios da tabela
def interpretar_entrada_tabela(entrada):
    if isinstance(entrada, str): #Verifica se a entrada é uma string para identificar empilha/reduz/aceita
        
        if entrada.startswith('E'):
            return ('empilha', int(entrada[1:]))
        
        elif entrada.startswith('R'):
            return ('reduz', int(entrada[1:]))
        
        elif entrada == 'AC':
            return ('aceita',)
    
    elif isinstance(entrada, (int, float)):
        #Entrada apenas de um numero representa um desvio
        return ('desvio', int(entrada))
    
    #Se a entrada nao é reconhecida, retorna None para erro de interpretaçao
    return None

#Gramatica
producoes = {
    0: ('<programa`>', ['<programa>']),
    1: ('<programa>', ['INICIO', '<decls>', '<instrucoes>', 'FIM']),
    2: ('<decls>', ['<decl>', '<decls>']),
    3: ('<decls>', []),  # Ɛ
    4: ('<decl>', ['Variavel', '<tipo>', '.']),
    5: ('<decl>', ['Variavel', '<atrib>']),
    6: ('<tipo>', ['INTEIRO']),
    7: ('<tipo>', ['REAL']),
    8: ('<tipo>', ['CARACTER']),
    9: ('<tipo>', ['ZEROUM']),
    10: ('<instrucoes>', ['<instrucao>', '<instrucoes>']),
    11: ('<instrucoes>', []),  # Ɛ
    12: ('<instrucao>', ['<atrib>']),
    13: ('<instrucao>', ['<atrib_teclado>']),
    14: ('<instrucao>', ['<escrever>']),
    15: ('<instrucao>', ['<condicional_se>']),
    16: ('<instrucao>', ['<loop_durante>']),
    17: ('<instrucao>', ['<loop_para>']),
    18: ('<atrib>', ['RECEBA', '<expr>', '.']),
    19: ('<atrib_teclado>', ['RECEBAT', 'Variavel', '.']),
    20: ('<escrever>', ['ESCREVA', '(', '<expr>', ')', '.']),
    21: ('<condicional_se>', ['SE', '(', '<expr>', ')', '{', '<instrucoes>', '}', '<senao_op>']),
    22: ('<senao_op>', ['SENAO', '{', '<instrucoes>', '}']),
    23: ('<senao_op>', []),  # Ɛ
    24: ('<loop_durante>', ['DURANTE', '(', '<expr>', ')', '{', '<instrucoes>', 'Variavel', '<inc_dec>', '}']),
    25: ('<loop_para>', ['PARA', '(', '<atrib>', '.', '<condicao>', '.', 'Variavel', '<inc_dec>', ')', '{', '<instrucoes>', '}']),
    26: ('<condicao>', ['<expr>', '<op_relacional>', '<expr>']),
    27: ('<inc_dec>', ['INC']),
    28: ('<inc_dec>', ['DEC']),
    29: ('<inc_dec>', ['<op_arit>', 'Num_inteiro']),
    30: ('<expr>', ['<term>', '<op>', '<term>']),
    31: ('<expr>', ['<term>']),
    32: ('<term>', ['Variavel']),
    33: ('<term>', ['Num_inteiro']),
    34: ('<term>', ['Num_real']),
    35: ('<term>', ['Caracter']),
    36: ('<term>', ['ZEROUM']),
    37: ('<op>', ['<op_relacional>']),
    38: ('<op>', ['<op_arit>']),
    39: ('<op>', ['<op_logico>']),
    40: ('<op_arit>', ['+']),
    41: ('<op_arit>', ['-']),
    42: ('<op_arit>', ['*']),
    43: ('<op_arit>', ['/']),
    44: ('<op_logico>', ['AND']),
    45: ('<op_logico>', ['OR']),
    46: ('<op_relacional>', ['>']),
    47: ('<op_relacional>', ['<']),
    48: ('<op_relacional>', ['IGUAL']),
    49: ('<op_relacional>', ['DIF']),
}


def analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes):
    pilha = [0]  #Estado inicial
    cursor = 0   #Índice do token atual

    while cursor < len(tokens1):
        estado_atual = pilha[-1]  #Estado no topo da pilha
        token_atual = tokens1[cursor][0]  #Obter o token atual (ex: 'INICIO')
        print("Estado atual:", estado_atual)
        print("Token atual:", token_atual)
        print("Pilha:", pilha)
        print()

       # Caso especial: se o token é 'op_relacional' e o estado é 100, substituir pelo lexema do próximo token
        if (token_atual == 'op_relacional' or token_atual == 'op_arit') and (estado_atual == 100 or estado_atual == 26):
            if cursor + 1 < len(tokens1):  # Verifica se há um próximo token
                lexema_proximo_token = tokens1[cursor][1]  # Obtém o lexema do próximo token
                print(f"Caso especial: substituindo 'op_relacional' por '{lexema_proximo_token}'")
                token_atual = lexema_proximo_token  # Substitui o token atual pelo lexema
            else:
                print("Erro: Não há próximo token para substituir 'op_relacional'.")
                return False
        
        elif token_atual == 'Variavel' and estado_atual == 56 :
            if cursor + 1 < len(tokens1):  # Verifica se há um próximo token
                print('Caso especial: pulando token ')
                token_atual = tokens1[cursor + 1][0]  # Substitui o token atual pelo lexema
                print(token_atual)
                cursor += 1
            else:
                print("Erro: Não há próximo token para substituir 'op_relacional'.")
                return False
        #Verifica se o token existe na tabela e se a entrada não é NaN 
        if token_atual in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_atual, token_atual]):
            acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
        else:

          
          print(f"Erro: Token '{token_atual}' não encontrado na tabela ou entrada inválida para o estado {estado_atual}.")
          print(tabela_SLR.loc[estado_atual, token_atual])
          return False

        print("Ação:", acao)
        print()

        if acao is None:
            print(f"Erro sintático: token inesperado '{token_atual}' na linha {tokens1[cursor][2]}")
            return False
        
        elif acao[0] == 'aceita':
            print("Aceitação: análise sintática concluída com sucesso.")
            return True
        
        elif acao[0] == 'empilha':
          #if cursor + 1 < len(tokens1) and tokens1[cursor+1][0] == 'Num_inteiro' and acao[1] == 53:
            #print("Caso especial: próximo token é um op_relacional")
            #print(tokens1[cursor + 1][1])
            #pilha = pilha[:-1]  # Remove o último estado da pilha
            #pilha.append(26)  # Adiciona o estado 
            #novo_estado = 26  # Pula para o estado
            #token_atual = tokens1[cursor][1]
            
            #cursor += 1
            
            # Verifica se há um próximo token e se ele é 'Variavel' e o estado é 53
          #elif cursor + 1 < len(tokens1) and tokens1[cursor + 1][0] == 'Variavel' and acao[1] == 53:
            #print("Caso especial: próximo token é Variavel")
            #pilha.append(token_atual)
            #pilha.append(26)
            #novo_estado = 26  # Usa o estado normal da ação
            #cursor += 1 
            


            
          # Caso padrão
          #else:
          novo_estado = acao[1]  # Usa o estado normal da ação
            
            
          pilha.append(token_atual)  #Empilha o token atual
          pilha.append(novo_estado)  #Empilha o novo estado
          cursor += 1  #Avança para o próximo token

        elif acao[0] == 'reduz':
            #print("token atual aaa: ", tokens1[cursor][0] )
            #print("ast atual aaa: ", acao[1] )
            if cursor + 1 < len(tokens1) and tokens1[cursor][0] == 'ESCREVA' and acao[1] == 5:
              print("Caso especial: próximo token é ESCREVA")
              pilha = pilha[:-1]  # Remove o último estado da pilha
              pilha.append(4)  # Adiciona o estado 4
              novo_estado = 34  # Pula para o estado 34
              continue

            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2  #O dobro na redução
            #Desempilha os elementos correspondentes à produção
            pilha = pilha[:-tamanho_producao]
            estado_topo = pilha[-1]

            #Transição de estado com o não-terminal reduzido
            if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
                desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
            else:
                print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
                return False

            #Verifica se a ação de desvio é válida
            if desvio and desvio[0] == 'desvio':
                pilha.append(nao_terminal)
                pilha.append(desvio[1])
            else:
                print(f"Erro: Ação de desvio inválida para o não-terminal '{nao_terminal}'")
                return False
        else:
            print("Erro: Ação desconhecida.")
            return False

    print("Erro: Fim inesperado da entrada.")
    return False


tokens1 = tokens_atualizados #tokens do lexico
analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes)
