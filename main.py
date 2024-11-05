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
    'e12': 'Num_Inteiro',
    'e15': 'Num_Real',
    'e16': 'Par_esquerdo',
    'e17': 'Par_direito',
    'e18': 'Ponto',
    'e19': 'Op_aritmetico',
    'e20': 'Op_relacional',
    'e23': 'Caracter',
    'e24': 'ERRO, numero_invalido',
    'e25': 'ERRO, ID_invalido',
    'e26': 'ERRO, nome_var_invalido',
    'e27': 'Chav_esquerda',
    'e28': 'Chav_direita'
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
    'INTEIRO': 'Tipo_var',
    'REAL': 'Tipo_var',
    'CARACTER': 'Tipo_var',
    'ZEROUM': 'Tipo_var',
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

#Imprime e salva a tabela de tokens no arquivo
def salvar_tokens_em_arquivo(nome_arquivo, tokens):
    with open(nome_arquivo, 'w') as arquivo:
        for token in tokens:
            #Escreve cada token em uma linha no arquivo
            arquivo.write(f"{token}\n")

print("\n Tabela de Tokens: \n")
for token in tokens_atualizados:
    print(token)
#
#  Salva a tabela de tokens atualizada em um arquivo
salvar_tokens_em_arquivo('tokens.txt', tokens_atualizados)

# ------------------------------- Sintático ---------------------------------------

# Carrega a tabela SLR do arquivo .xlsx
def carregar_tabela_SLR(caminho_arquivo):
    # Carrega a planilha, assumindo que a primeira linha é o cabeçalho com os símbolos (terminais e não-terminais)
    tabela = pd.read_excel(caminho_arquivo, index_col=0)  # index_col=0 define a primeira coluna como índices (estados)
    return tabela

# Interpreta as entradas da tabela SLR
def interpretar_entrada_tabela(entrada):
    if pd.isna(entrada):  # Verifica se a célula está vazia
        return None
    elif entrada == 'AC':
        return ('aceita', None)
    elif entrada.startswith('E'):
        return ('empilha', int(entrada[1:]))  # Ex: 'E3' -> (empilha, 3)
    elif entrada.startswith('R'):
        return ('reduz', int(entrada[1:]))  # Rx: 'R2' -> (reduz, 2)
    else:
        return ('desvio', int(entrada))  # Apenas um número indica desvio para o estado

# Define a gramática: lista de produções (não-terminal, [lista de símbolos do lado direito])
producoes = {
    0: ('<Programa`>', ['Programa']),
    1: ('Programa', ['INICIO', '<decls>', '<instrucoes>', 'FIM']),
    2: ('DECLS', ['DECL', 'DECLS']),
    3: ('DECLS', []),  # Ɛ
    4: ('DECL', ['Variavel', 'TIPO', '.']),
    5: ('TIPO', ['INTEIRO']),
    6: ('TIPO', ['REAL']),
    7: ('TIPO', ['CARACTER']),
    8: ('TIPO', ['ZEROUM']),
    9: ('INSTRUCOES', ['INSTRUCAO', 'INSTRUCOES']),
    10: ('INSTRUCOES', []),  # Ɛ
    11: ('INSTRUCAO', ['ATRIB']),
    12: ('INSTRUCAO', ['ATRIB_TECLADO']),
    13: ('INSTRUCAO', ['ESCREVER']),
    14: ('INSTRUCAO', ['CONDICIONAL_SE']),
    15: ('INSTRUCAO', ['LOOP_DURANTE']),
    16: ('INSTRUCAO', ['LOOP_PARA']),
    17: ('ATRIB', ['Variavel', 'RECEBA', 'EXPR', '.']),
    18: ('ATRIB_TECLADO', ['RECEBAT', 'Variavel', '.']),
    19: ('ESCREVER', ['ESCREVA', '(', 'EXPR', ')', '.']),
    20: ('CONDICIONAL_SE', ['SE', '(', 'EXPR', ')', '{', 'INSTRUCOES', '}', 'SENAO_OP']),
    21: ('SENAO_OP', ['SENAO', '{', 'INSTRUCOES', '}']),
    22: ('SENAO_OP', []),  # Ɛ
    23: ('LOOP_DURANTE', ['DURANTE', '(', 'EXPR', ')', '{', 'INSTRUCOES', 'Variavel', 'INC_DEC', '}']),
    24: ('LOOP_PARA', ['PARA', '(', 'ATRIB', '.', 'CONDICAO', '.', 'Variavel', 'INC_DEC', ')', '{', 'INSTRUCOES', '}']),
    25: ('CONDICAO', ['EXPR', 'OP_RELACIONAL', 'EXPR']),
    26: ('INC_DEC', ['INC']),
    27: ('INC_DEC', ['DEC']),
    28: ('INC_DEC', ['OP_ARIT', 'Num_inteiro']),
    29: ('EXPR', ['TERM', 'OP', 'TERM']),
    30: ('EXPR', ['TERM']),
    31: ('TERM', ['Num_inteiro']),
    32: ('TERM', ['Num_real']),
    33: ('TERM', ['Caracter']),
    34: ('TERM', ['ZEROUM']),
    35: ('OP', ['OP_RELACIONAL']),
    36: ('OP', ['OP_ARIT']),
    37: ('OP', ['OP_LOGICO']),
    38: ('OP_ARIT', ['+']),
    39: ('OP_ARIT', ['-']),
    40: ('OP_ARIT', ['*']),
    41: ('OP_ARIT', ['/']),
    42: ('OP_LOGICO', ['AND']),
    43: ('OP_LOGICO', ['OR']),
    44: ('OP_RELACIONAL', ['>']),
    45: ('OP_RELACIONAL', ['<']),
    46: ('OP_RELACIONAL', ['IGUAL']),
    47: ('OP_RELACIONAL', ['DIF']),
}

# Caminho para o arquivo Excel
caminho_arquivo = 'Tabela_SLR.xlsx'
tabela_SLR = carregar_tabela_SLR(caminho_arquivo)
print("Tabela SLR Carregada.")

# Analisador Sintático SLR
def analisador_sintatico(tokens, tabela_SLR, producoes):
    pilha = [0]  # Estado inicial é 0
    cursor = 0   # Índice do token atual
    while cursor < len(tokens):
        estado_atual = pilha[-1]  # Estado no topo da pilha
        token_atual = tokens[cursor][0]  # Obter o token atual (ex: 'ID', 'NUM')

        # Busca a ação na tabela SLR
        acao = interpretar_entrada_tabela(tabela_SLR.loc[estado_atual, token_atual])

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
            cursor += 1  # Avança para o próximo token
        elif acao[0] == 'reduz':
            num_producao = acao[1]
            nao_terminal, producao = producoes[num_producao]
            tamanho_producao = len(producao) * 2  # Dobra o tamanho devido aos estados na pilha
            
            # Desempilha os elementos correspondentes à produção
            pilha = pilha[:-tamanho_producao]
            estado_topo = pilha[-1]
            
            # Transição de estado com o não-terminal reduzido
            desvio = interpretar_entrada_tabela(tabela_SLR.loc[estado_topo, nao_terminal])
            if desvio is None or desvio[0] != 'desvio':
                print(f"Erro de desvio: não-terminal '{nao_terminal}' inesperado após redução.")
                return False
            
            # Empilha o não-terminal e o novo estado de desvio
            pilha.append(nao_terminal)
            pilha.append(desvio[1])
        else:
            print("Erro: Ação desconhecida.")
            return False

    print("Erro: Fim inesperado da entrada.")
    return False

# Executa o analisador sintático com os tokens gerados e a tabela SLR carregada
tokens = tokens_atualizados  # Assume que a lista tokens_atualizados está preenchida com os tokens do léxico
analisador_sintatico(tokens, tabela_SLR, producoes)