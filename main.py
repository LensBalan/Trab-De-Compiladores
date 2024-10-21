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
    'e23': 'String',
    'e24': 'ERRO, numero_invalido',
    'e25': 'ERRO, ID_invalido',
    'e26': 'ERRO, nome_var_invalido',
    'e27': 'Chav_esquerda',
    'e28': 'Chav_direita'
}

# Função para processar o arquivo e reconhecer os tokens
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

print("\n Tabela de Tokens: \n")
for token in tokens_atualizados:
    print(token)



#------------------------------------- Sintatico -------------------------------------------


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Posição atual na lista de tokens

    def proximo_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo_esperado):
        token = self.proximo_token()
        if token and token[0] == tipo_esperado:
            self.pos += 1  # Avança para o próximo token
        else:
            raise SyntaxError(f"Erro de sintaxe: esperado {tipo_esperado}, mas encontrado {token}")

    def analisar(self):
        self.programa()

    def programa(self):
        # Regra de produção: Programa -> INICIO Bloco FIM
        self.consumir('INICIO')
        self.bloco()
        self.consumir('FIM')

    def bloco(self):
        # Regra de produção: Bloco -> { Declarações }
        self.consumir('Chav_esquerda')
        while self.proximo_token()[0] != 'Chav_direita':
            self.declaracao()
        self.consumir('Chav_direita')

    def declaracao(self):
        # Exemplo de uma declaração: Tipo_var ID .
        tipo = ['INTEIRO', 'REAL', 'CARACTER', 'ZEROUM']
        if self.proximo_token()[0] in tipo:
            self.consumir(self.proximo_token()[0])  # Consome o tipo
            self.consumir('ID')  # Consome o identificador
            self.consumir('.')   # Consome o ponto final
        else:
            raise SyntaxError("Erro de sintaxe: tipo de variável esperado")

    def atribuicao(self):
        # Regra de produção: Atribuicao -> ID RECEBA Expressao .
        self.consumir('ID')
        self.consumir('RECEBA')
        self.expressao()
        self.consumir('.')

    def expressao(self):
        # Aqui você deve definir a lógica para expressões, como operadores
        # Exemplo simples: ID | NUMERO | '...' (ou algo semelhante)
        if self.proximo_token()[0] == 'ID':
            self.consumir('ID')
        elif self.proximo_token()[0] == 'NUMERO':
            self.consumir('NUMERO')
        elif self.proximo_token()[0] == 'STRING':
            self.consumir('STRING')
        else:
            raise SyntaxError("Erro de sintaxe: expressão esperada")

    def comando_escrever(self):
        # Regra de produção: ESCRITA -> ESCREVA ( Expressao )
        self.consumir('ESCREVA')
        self.consumir('(')
        self.expressao()
        self.consumir(')')

    def comando_se(self):
        # Regra de produção: SE ( Condicao ) { Bloco } [ SENAO { Bloco } ]
        self.consumir('SE')
        self.consumir('(')
        self.condicao()
        self.consumir(')')
        self.consumir('Chav_esquerda')
        self.bloco()
        self.consumir('Chav_direita')
        if self.proximo_token()[0] == 'SENAO':
            self.consumir('SENAO')
            self.consumir('Chav_esquerda')
            self.bloco()
            self.consumir('Chav_direita')

    def condicao(self):
        # Defina a condição de comparação, por exemplo: x > y
        self.consumir('ID')  # Exemplo: primeira variável
        operador = ['>', 'DIF', '<', '>=', '<=', '==']
        if self.proximo_token()[0] in operador:
            self.consumir(self.proximo_token()[0])  # Consome o operador
            self.consumir('ID')  # Exemplo: segunda variável
        else:
            raise SyntaxError("Erro de sintaxe: operador esperado")

    def comando_durante(self):
        # Regra de produção: DURANTE ( Condicao ) { Bloco }
        self.consumir('DURANTE')
        self.consumir('(')
        self.condicao()
        self.consumir(')')
        self.consumir('Chav_esquerda')
        self.bloco()
        self.consumir('Chav_direita')

    def comando_para(self):
        # Regra de produção: PARA ( Atribuicao ; Condicao ; Atribuicao ) { Bloco }
        self.consumir('PARA')
        self.consumir('(')
        self.atribuição()
        self.consumir(';')
        self.condicao()
        self.consumir(';')
        self.atribuição()
        self.consumir(')')
        self.consumir('Chav_esquerda')
        self.bloco()
        self.consumir('Chav_direita')

# Função principal para executar o analisador
def main():
 
    # Inicializa o analisador sintático com os tokens atualizados
    analisador = AnalisadorSintatico(tokens_atualizados)
    
    try:
        analisador.analisar()
        print("Análise sintática concluída com sucesso!")
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    main()
