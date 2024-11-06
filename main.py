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
        #if 'a' <= caracter <= 'z':
       #  return 'e22'
      #  if 'A' <= caracter <= 'Z':
       #   return 'e22'
       # if '0' <= caracter <= '9':
       #   return 'e22'
      #  if caracter == ' ':
      #    return 'e22'
      ##  if '\u0021' <= caracter <= '\u002F':  # inclui !"#$%&'()*+-./
       #   return 'e22'
      #  if '\u003A' <= caracter <= '\u0040':  # inclui : ; < = > ? @
        #  return 'e22'
      #  if '\u005B' <= caracter <= '\u0060' and caracter != '^':  #inclui [\]_`
        #  return 'e22'
    elif estado == 'e22':
       # if 'a' <= caracter <= 'z':
      #    return 'e22'
      #  if 'A' <= caracter <= 'Z':
      #    return 'e22'
      #  if '0' <= caracter <= '9':
      #    return 'e22'
       # if caracter == ' ':
      #    return 'e22'
#if '\u0021' <= caracter <= '\u002F':  # inclui !"#$%&'()*+-./
      #    return 'e22'
      #  if '\u003A' <= caracter <= '\u0040':  # inclui : ; < = > ? @
      #    return 'e22'
      #  if '\u005B' <= caracter <= '\u0060' and caracter != '^':  #inclui [\]_`
     #     return 'e22'
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
    'e19': 'Op_arit',
    'e20': 'Op_relacional',
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
    'DIF': 'Op_relacional',
    'IGUAL': 'Op_relacional',
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
    print(token)


# ------------------------------- Sintático ---------------------------------------

def carregar_tabela_SLR(arq):
    #Carrega a planilha
    tabela = pd.read_excel(arq, index_col=0)  # index_col=0 define a primeira coluna comoos estados
    return tabela

# Caminho para o arquivo Excel
arq = 'Tabela_SLR.xlsx'
tabela_SLR = carregar_tabela_SLR(arq)
print("Tabela SLR Carregada.")
print()

#Interpretar E, R, AC e desvios da tabela
def interpretar_entrada_tabela(entrada):
    #Verifica se a entrada é uma string para identificar empilha/reduz/aceita
    if isinstance(entrada, str):
        
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
    5: ('<tipo>', ['INTEIRO']),
    6: ('<tipo>', ['REAL']),
    7: ('<tipo>', ['CARACTER']),
    8: ('<tipo>', ['ZEROUM']),
    9: ('<instrucoes>', ['<instrucao>', '<instrucoes>']),
    10: ('<instrucoes>', []),  # Ɛ
    11: ('<instrucao>', ['<atrib>']),
    12: ('<instrucao>', ['<atrib_teclado>']),
    13: ('<instrucao>', ['<escrever>']),
    14: ('<instrucao>', ['<condicional_se>']),
    15: ('<instrucao>', ['<loop_durante>']),
    16: ('<instrucao>', ['<loop_para>']),
    17: ('<atrib>', ['Variavel', 'RECEBA', '<expr>', '.']),
    18: ('<atrib_teclado>', ['RECEBAT', 'Variavel', '.']),
    19: ('<escrever>', ['ESCREVA', '(', '<expr>', ')', '.']),
    20: ('<condicional_se>', ['SE', '(', '<expr>', ')', '{', '<instrucoes>', '}', '<senao_op>']),
    21: ('<senao_op>', ['SENAO', '{', '<instrucoes>', '}']),
    22: ('<senao_op>', []),  # Ɛ
    23: ('<loop_durante>', ['DURANTE', '(', '<expr>', ')', '{', '<instrucoes>', 'Variavel', '<inc_dec>', '}']),
    24: ('<loop_para>', ['PARA', '(', '<atrib>', '.', '<condicao>', '.', 'Variavel', '<inc_dec>', ')', '{', '<instrucoes>', '}']),
    25: ('<condicao>', ['<expr>', '<op_relacional>', '<expr>']),
    26: ('<inc_dec>', ['INC']),
    27: ('<inc_dec>', ['DEC']),
    28: ('<inc_dec>', ['<op_arit>', 'Num_inteiro']),
    29: ('<expr>', ['<term>', '<op>', '<term>']),
    30: ('<expr>', ['<term>']),
    31: ('<term>', ['Num_inteiro']),
    32: ('<term>', ['Num_real']),
    33: ('<term>', ['Caracter']),
    34: ('<term>', ['ZEROUM']),
    35: ('<op>', ['<op_relacional>']),
    36: ('<op>', ['<op_arit>']),
    37: ('<op>', ['<op_logico>']),
    38: ('<op_arit>', ['+']),
    39: ('<op_arit>', ['-']),
    40: ('<op_arit>', ['*']),
    41: ('<op_arit>', ['/']),
    42: ('<op_logico>', ['AND']),
    43: ('<op_logico>', ['OR']),
    44: ('<op_relacional>', ['>']),
    45: ('<op_relacional>', ['<']),
    46: ('<op_relacional>', ['IGUAL']),
    47: ('<op_relacional>', ['DIF']),
}


def analisador_sintatico_bottom_up(tokens, tabela_SLR, producoes):
    pilha = [0]  #Estado inicial
    cursor = 0   #indice do token atual

    while cursor < len(tokens):
        estado_atual = pilha[-1]  #Estado no topo da pilha
        token_atual = tokens[cursor][0]  #Obter o token atual (ex: 'INICIO', 'PARA')
        print("Estado atual:", estado_atual)
        print("Token atual:", token_atual)

        #Verifica se o token existe na tabela e se a entrada não é NaN (vazio)
        if token_atual in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_atual, token_atual]):
            acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])
        else:
            print(f"Erro: Token '{token_atual}' não encontrado na tabela ou entrada invalida para o estado {estado_atual}.")
            return False

        print("Ação:", acao)
        print()

        if acao is None:
            print(f"Erro sintático: token inesperado '{token_atual}' na linha {tokens[cursor][2]}")
            return False
        elif acao[0] == 'aceita':
            print("Aceitação: análise sintática concluída com sucesso.")
            return True
        elif acao[0] == 'empilha':
            novo_estado = acao[1]
            pilha.append(token_atual)  # Empilha o token atual
            pilha.append(novo_estado)  # Empilha o novo estado
            cursor += 1  #Avança para o prox token
        elif acao[0] == 'reduz':
            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2  #O dobro na reduçao
            #Desempilha os elementos correspondentes a prod
            pilha = pilha[:-tamanho_producao]
            estado_topo = pilha[-1]

            #Transição de estado com o não-terminal reduzido
            if nao_terminal in tabela_SLR.columns and not pd.isna(tabela_SLR.loc[estado_topo, nao_terminal]):
                desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
            else:
                print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
                return False

            # erifica se a ação de desvio é valida
            if desvio and desvio[0] == 'desvio':
                pilha.append(nao_terminal)
                pilha.append(desvio[1])
            else:
                print(f"Erro: Ação de desvio invalida para o não-terminal '{nao_terminal}'")
                return False
        else:
            print("Erro: Ação desconhecida.")
            return False

    print("Erro: Fim inesperado da entrada.")
    return False


tokens1 = tokens_atualizados #tokens do lexico
analisador_sintatico_bottom_up(tokens1, tabela_SLR, producoes)