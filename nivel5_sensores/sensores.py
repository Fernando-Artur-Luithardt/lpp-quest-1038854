"""NÍVEL 5 — Vulcão dos Sensores (Python)

Sensores de temperatura (IoT) mandam leituras, mas algumas vêm quebradas (None) ou absurdas.
Você vai usar RECURSÃO para percorrer listas sem laços e juntar tudo num painel de monitoramento.
Siga as missões na ordem e rode  python quest.py 5  a cada passo (veja o LEIAME.md).

Uma leitura é um número (°C) ou None (falha do sensor). Leitura VÁLIDA: número entre -40 e 85, inclusive.
"""

LIMITE_MIN = -40
LIMITE_MAX = 85


# ============================================================ MISSÃO 5.1 — Recursão: o básico
# Receita da recursão:  (1) caso base: a lista vazia tem resposta direta;
#                       (2) passo: resolva o primeiro item e deixe o RESTO (valores[1:]) para a própria função.
def somar(valores):
    """Soma dos valores, recursivamente. Lista vazia: 0.   somar([1, 2, 3]) -> 6"""
    return 0 if not valores else valores[0] + somar(valores[1:])


def contar(valores, predicado):
    """Quantos valores satisfazem o predicado (função que devolve True/False), recursivamente.
    contar([1, 5, 9], lambda x: x > 4) -> 2
    """
    return 0 if not valores else int(bool(predicado(valores[0]))) + contar(valores[1:], predicado)


def maximo(valores):
    """Maior valor, recursivamente. Lista vazia: None."""
    if not valores:
        return None
    resto = maximo(valores[1:])
    return valores[0] if resto is None or valores[0] > resto else resto


# ============================================================ MISSÃO 5.2 — Limpar e janelas
def limpar(leituras):
    """Lista NOVA só com as leituras válidas (nem None, nem fora do intervalo -40..85), na mesma ordem."""
    return list(filter(_valida, leituras))


def media_movel(valores, janela):
    """Média de cada janela de `janela` valores consecutivos, arredondada a 2 casas.
    media_movel([1, 2, 3, 4], 2) -> [1.5, 2.5, 3.5]
    Lista menor que a janela: []. Dica: comprehension com fatias valores[i:i + janela].
    """
    if janela <= 0:
        raise ValueError("A janela deve ser positiva")
    return list(map(
        lambda i: round(somar(valores[i:i + janela]) / janela, 2),
        range(len(valores) - janela + 1),
    ))


# ============================================================ MISSÃO 5.3 — Alertas e o painel final
def detectar_alertas(leituras, limite):
    """Lista de {"indice": i, "valor": v} das leituras VÁLIDAS acima do limite (índice na lista ORIGINAL).

    Dica: enumerate(leituras) dá (indice, valor); filtre com uma comprehension.
    """
    return list(map(
        lambda par: {"indice": par[0], "valor": par[1]},
        filter(lambda par: _valida(par[1]) and par[1] > limite, enumerate(leituras)),
    ))


def resumo_sensores(sensores, limite):
    """sensores: {"s1": [leituras...], "s2": [...]}. Devolve, para cada sensor:
    {"validas": nº de leituras válidas, "media": média das válidas (2 casas, 0.0 se não houver), "alertas": nº de alertas}

    Use limpar, detectar_alertas e as funções anteriores. Sem laços e sem alterar a entrada!
    """
    def resumir(item):
        nome, leituras = item
        validas = limpar(leituras)
        return nome, {
            "validas": len(validas),
            "media": round(somar(validas) / len(validas), 2) if validas else 0.0,
            "alertas": len(detectar_alertas(leituras, limite)),
        }

    return dict(map(resumir, sensores.items()))


def _valida(valor):
    return isinstance(valor, (int, float)) and LIMITE_MIN <= valor <= LIMITE_MAX
