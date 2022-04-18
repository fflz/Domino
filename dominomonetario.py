import random



def gerar_pecas(pecas):
    # gera combinações de peças de 0 até 11 (12)
    for i in range(12):
        for j in range(i, 12):
           pecas.append([i, j])
    random.shuffle(pecas) # embaralha as peças


def jogar_primeira_peca(computador, jogador):
    # percorre a mão do computador e do jogador para ver quem tem a combinação mais alta para começar o jogo de acordo com as regras
    for i in reversed(range(12)):
        if [i, i] in computador:
            return computador.pop(computador.index([i, i])) # pop pq ele irá remover a peça da mão do computador e jogar na mesa assim o computador começa
        if [i, i] in jogador:
            return jogador.pop(jogador.index([i, i])) # pop pq ele irá remover a peça da mão do jogador e jogar na mesa assim o jogador começa
    return None


def distribuir_maos(banco, jogador, pecas_iniciais): 
    # distribuir as peças na mão
    jogador.extend(banco[:pecas_iniciais])
    for item in jogador:
        banco.remove(item) # como o banco tem todas as peças, ele remove de lá e coloca na mão do usuario


def comecar(banco, computador, jogador, tela):
    while True:
        gerar_pecas(banco) # cria o conjunto de peças
        distribuir_maos(banco, computador, pecas_iniciais=12) # distribui 12 peças para a CPU; 12 pode ser mudado, coloquei 12 seguindo o PDF do domino monetario (12 ou 13 peças)
        distribuir_maos(banco, jogador, pecas_iniciais=12) # distribui 12 peças para o JOGADOR
        first_piece = jogar_primeira_peca(computador, jogador) # busca a peça mais alta pra saber quem começa
        if len(computador) == len(jogador):
            banco.clear()
            jogador.clear()
            computador.clear()
            tela.clear()
            continue
        tela.append(first_piece)
        break


def mostrar_mao(mao):
    # função simples para printar todas as peças na mão do jogador
    for i, peca in enumerate(mao):
        print(f'{i + 1}: {peca}')


def printar_jogo(domino_tela):
    # se o numero de peças na mesa for muito grande, oculta as primeiras peças jogandas com ... para facilitar e nao poluir a tela
    if len(domino_tela) > 6:
        interface_direita = str(domino_tela[0:3])[1:- 1]
        interface_esquerda = str(domino_tela[-3:])[1: - 1]
        tela = f'{interface_direita}...{interface_esquerda}'
    else:
        tela = str(domino_tela)[1: - 1]
    print(tela)


def printar_status(pecas_jogador, pecas_computador, indicador_turno, players, acabou):
    # função simples apenas para dizer se o jogador ganhou, perdeu, empatou e que é sua vez de jogar
    if acabou:
        if len(pecas_jogador) == 0 or len(pecas_jogador) < len(pecas_computador):
            status = 'O jogo acabou, você ganhou!'
        elif len(pecas_computador) == 0 or len(pecas_computador) < len(pecas_jogador):
            status = 'O jogo acabou, o computador venceu!'
        else:
            status = "O jogo acabou em um empatado!" # empate = jogo fechado, quando não é mais possível baixar peças, geralmente quando as duas pontas do jogo têm o mesmo número e não existem mais 
                                                   # peças com este número na mão dos jogadores, nem a serem compradas.
    elif players[indicador_turno] == 'computador':
        status = 'O computador vai fazer sua jogada, aperte ENTER'
    else:
        status = "É seu turno, escolha uma opção para jogar!"
    print(f'Status: {status}')


def printar_interface(banco, computador, jogador, tela, turno, players, acabou):
    print('=' * 120)
    print(f'Tamanho do banco: {len(banco)}')
    print(f'Peças do computador: {len(computador)}')
    print()
    printar_jogo(tela)
    print()
    print('Suas peças:')
    mostrar_mao(jogador)
    printar_status(jogador, computador, turno, players, acabou)


def jogador_valido(pecas):
    # verifica se a entrada do jogador é valida, lembrando que ele tem um conjunto de peças que vai de 1 até o numero de peças na mão
    # e deve escolher a opção que representa a peça que quer jogar 
    input_string = input()
    if not input_string.lstrip("-").isdigit():
        print('Comando invalido, tente novamente.')
        return jogador_valido(pecas)
    move = int(input_string)
    if abs(move) > pecas:
        print('Comando invalido, tente novamente.')
        return jogador_valido(pecas)
    return move


def gere_interface(tela): # função simples apenas para realizar a contagem das peças na mesa
    for i in range(12):
        if str(tela).count(str(i)) == 9:
            return True
    return False


def gere_maos(tela, computador, jogador, banco): # gere a mão do jogador e da cpu em questão de interface
    pode_mover = True
    if not banco:
        for peca in computador:
            if lado_esquerdo(tela, peca) or lado_direito(tela, peca):
                pode_mover = False
        for peca in jogador:
            if lado_esquerdo(tela, peca) or lado_direito(tela, peca):
                pode_mover = False
    else:
        pode_mover = False
    return pode_mover


def lado_esquerdo(domino_tela, _pecas_jogador):
    fim = domino_tela[0][0]
    return fim in _pecas_jogador


def lado_direito(domino_tela, _pecas_jogador):
    fim = domino_tela[-1][1]
    return fim in _pecas_jogador


def turno_peca(domino_tela, peca, lado):
    if lado > 0:
        if domino_tela[-1][1] != peca[0]:
            peca.reverse()
    else:
        if domino_tela[0][0] != peca[1]:
            peca.reverse()


def jogador_joga(pecas_jogador, pecas_banco, domino_tela):
    while True:
        move = jogador_valido(len(pecas_jogador)) # checa se o que o jogador digitou é uma opção de peça que ele tem em mãos
        peca_jogador = pecas_jogador[abs(move) - 1] # moveu a peça, logo remove ela da mão 
        # se a entrada do jogador for 0 ele irá comprar uma peça e remover ela da pilha de peças
        # pilha de peças é definida na função game() 
        if move == 0:
            if len(pecas_banco) != 0:
                pecas_jogador.append(pecas_banco.pop(random.randint(0, len(pecas_banco) - 1)))
            break
        elif move < 0 and lado_esquerdo(domino_tela, peca_jogador):
            pecas_jogador.remove(peca_jogador) # jogou a peça do lado esquerdo e remove da mão
            turno_peca(domino_tela, peca_jogador, move) 
            domino_tela.insert(0, peca_jogador) # insere a peça na mesa 
            break
        elif lado_direito(domino_tela, peca_jogador):
            pecas_jogador.remove(peca_jogador) # jogou a peça do lado direito e remove da mão
            turno_peca(domino_tela, peca_jogador, move)
            domino_tela.append(peca_jogador) # insere a peça na mesa 
            break
        else:
            print('Jogada ilegal, tente novamente.')
            continue


def calcular_numeros(pecas_computador, domino_tela): # aqui calculamos o valor da peça para saber na função peso_mao qual o peso de cada peça afim de jogar
    _peso_numero = dict()
    peca_visivel = []
    peca_visivel.extend(pecas_computador)
    peca_visivel.extend(domino_tela)
    for i in range(12):
        count = 0
        for item in peca_visivel:
            if item == [i, i]: # se a peça é dupla (6,6) por exemplo então ela tem o peso 2, lembrando que é com base na peça (direita, esquerda) que está na tela
                count += 2
            elif i in item: # se a peça não é dupla (1,6) ela tem o peso 1
                count += 1
        _peso_numero[i] = count 
    return _peso_numero


def peso_mao(peso_numero, pecas_computador):
    peso_pecas = dict()
    for index, item in enumerate(pecas_computador):
        peso_peca = peso_numero[item[0]] + peso_numero[item[1]]
        peso_pecas[index] = peso_peca

    chaves_ordenadas = sorted(peso_pecas, key=peso_pecas.get)  # [1, 3, 2]
    computador_ordenadas = list(pecas_computador)
    for i, val in enumerate(chaves_ordenadas):
        pecas_computador[i] = computador_ordenadas[val]
    pecas_computador.reverse()


def computadorAI_jogar(pecas_computador, pecas_banco, domino_tela):
    input()
    peso_numero = calcular_numeros(pecas_computador, domino_tela) # calcula o peso das peças do computador em consideração com as peças na mesa
    peso_mao(peso_numero, pecas_computador) # calcula o peso total da mão pra saber o que jogar 
    for peca in pecas_computador: # a partir daqui ele joga, e gere a interface(mesa)
        if lado_esquerdo(domino_tela, peca): 
            pecas_computador.remove(peca) # remove da mão do computador 
            turno_peca(domino_tela, peca, lado=-1) 
            domino_tela.insert(0, peca) # insere na interface(mesa)
            break
        if lado_direito(domino_tela, peca):
            pecas_computador.remove(peca)
            turno_peca(domino_tela, peca, lado=1)
            domino_tela.append(peca)
            break
    else:
        if len(pecas_banco) != 0: # contanto que o banco nao esteja vazio e não tenha peças para jogar o computador COMPRA
            pecas_computador.append(pecas_banco.pop(random.randint(0, len(pecas_banco) - 1))) # apesar de usar RANDOM nao tem ligação com a heuristica, é apenas uma compra aleatoria de peça que esta no banco


def game():
    pecas_banco, pecas_computador, pecas_jogador, domino_tela = [], [], [], []
    # a função abaixo ja deixa declarado as peças, porem a função gerar_pecas(pecas) pode gerar peças diferentes
    # deixei comentada pois planejava modificar para deixar o formato como o domino monetario porém centavos seria necessario ser float 0.25, 0.50
    # mas existem outras soluções, como fazer um dicionario, e outras coisas
    # pecas_banco = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1,8], [1, 9], [1, 10], [1, 11], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [2, 11], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [3, 11], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [4, 11], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 6], [6, 7], [6, 8], [6, 9], [6, 10], [6, 11], [7, 7], [7, 8], [7, 9], [7, 10], [7, 11], [8, 8], [8, 9], [8, 10], [8, 11], [9, 9], [9, 10], [9, 11], [10, 10], [10, 11], [11, 11]]
    players = ('jogador', 'computador')
    comecar(banco=pecas_banco, computador=pecas_computador, jogador=pecas_jogador, tela=domino_tela)
    indicador_turno = 1 if len(pecas_jogador) < len(pecas_computador) else 0

    while True:
        acabou = gere_interface(domino_tela) \
                  or gere_maos(domino_tela, pecas_computador, pecas_jogador, pecas_banco) \
                  or len(pecas_computador) == 0 or len(pecas_jogador) == 0
        printar_interface(banco=pecas_banco,
                        computador=pecas_computador,
                        jogador=pecas_jogador,
                        tela=domino_tela,
                        turno=indicador_turno,
                        players=players,
                        acabou=acabou)
        if acabou:
            break
        if players[indicador_turno] == 'jogador':
            #jogador_joga(pecas_jogador=pecas_jogador, pecas_banco=pecas_banco, domino_tela=domino_tela)
            computadorAI_jogar(pecas_computador=pecas_jogador, pecas_banco=pecas_banco, domino_tela=domino_tela) # fazer a cpu jogar contra ela mesma
        else:
            computadorAI_jogar(pecas_computador=pecas_computador, pecas_banco=pecas_banco, domino_tela=domino_tela)
        indicador_turno = (indicador_turno + 1) % len(players)


game()