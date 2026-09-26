class SistemaEspecialista:
    """Guarda a base de conhecimento e implementa inferência e explicação."""

    # Vamos usar só fatos POSITIVOS como nos exemplos do Vinicius:
    # Checar: Unidade-2_e_3.pdf, slide 38

    def __init__(self):
        # CATEGORIAS: agrupam as regras para que o usuário responda apenas às perguntas relacionadas ao tipo de problema que está enfrentando.
        # chave = identificador interno | valor = texto exibido no menu
        self.categorias = {
            "energia": "Não liga / tela preta",
            "desempenho": "Lentidão / ruídos no disco",
            "temperatura": "Desliga ou reinicia sozinho",
            "tela": "Tela azul / defeitos na imagem",
            "rede": "Sem internet",
        }

        # BASE DE CONHECIMENTO
        # Cada fato da base corresponde a 1 pergunta de sim/não.
        # chave = nome do fato | valor = texto mostrado ao usuário
        self.perguntas = {
            # perguntas energia
            "sem_energia": "Ao apertar o botão, o computador fica totalmente sem sinal (nenhuma luz, som ou ventoinha)?",
            "pc_liga": "O computador liga ao apertar o botão (ventoinhas giram)?",
            "emite_bips": "O computador emite bipes ao ligar?",
            "tela_preta": "A tela permanece preta depois de ligar?",
            # perguntas desempenho
            "lento": "O computador está lento no uso geral?",
            "disco_100": "No Gerenciador de Tarefas, o uso do disco fica próximo de 100%?",
            "hd_ruido": "O HD faz ruídos anormais (cliques, arranhados)?",
            "popups": "Aparecem pop-ups ou anúncios inesperados?",
            # perguntas temperatura
            "desliga_sozinho": "O computador desliga sozinho?",
            "gabinete_quente": "O gabinete fica muito quente ao toque?",
            "reinicia_sozinho": "O computador reinicia sozinho, aleatoriamente?",
            "poeira_coolers": "Há acúmulo visível de poeira nos coolers?",
            # perguntas tela
            "tela_azul_frequente": "Ocorrem telas azuis (BSOD) com frequência?",
            "artefatos_tela": "Aparecem artefatos na tela (riscos, quadrados, cores estranhas)?",
            "trava_jogos_videos": "O computador trava durante jogos ou vídeos?",
            # perguntas rede
            "sem_internet": "O computador está sem conexão com a internet?",
            "outros_dispositivos_conectam": "Outros dispositivos da mesma rede conectam normalmente?",
        }

        # BASE DE CONHECIMENTO - REGRAS SE-ENTÃO
        # "se"      -> conjunto de fatos que precisam ser TODOS verdadeiros
        #              Ex.: {"lento", "disco_100"}
        # "entao"   -> diagnóstico
        # "acao"    -> o que o usuário deve fazer
        # "tecnico" -> True se o reparo exige assistência técnica

        # Condições com "não" são escritas como um fato positivo
        # Ex.: "não liga e sem luzes/sons" -> "sem_energia"

        # Condições com OU viram DUAS regras com a mesma conclusão
        # Checar: Unidade-2_e_3.pdf, slide 37

        # A R11 ñ está aqui: ela não tem condição própria.
        # Vamos tratar como o caso em que nenhuma regra dispara (mostrar_resultado())
        # Checar: Unidade-2_e_3.pdf, slide 38, linha 23
        self.regras = [
            # Categoria: energia
            {
                "id": "R1", "categoria": "energia",
                "se": {"sem_energia"},
                "entao": "Fonte de alimentação defeituosa.",
                "acao": "Teste em outra tomada e com outro cabo de energia. "
                        "Persistindo, a fonte deve ser substituída.",
                "tecnico": True,
            },
            {
                "id": "R2a", "categoria": "energia",
                "se": {"pc_liga", "emite_bips"},
                "entao": "Memória RAM com defeito.",
                "acao": "Com o computador desligado e fora da tomada, "
                        "retire e reencaixe os pentes de memória.",
                "tecnico": True,
            },
            {
                "id": "R2b", "categoria": "energia",
                "se": {"pc_liga", "tela_preta"},
                "entao": "Memória RAM com defeito.",
                "acao": "Com o computador desligado e fora da tomada, "
                        "retire e reencaixe os pentes de memória.",
                "tecnico": True,
            },
            # Categoria: desempenho
            {
                "id": "R4", "categoria": "desempenho",
                "se": {"lento", "disco_100"},
                "entao": "Disco rígido (HD) ou SSD com falha.",
                "acao": "Faça backup dos arquivos importantes e verifique a "
                        "saúde do disco com uma ferramenta de diagnóstico.",
                "tecnico": True,
            },
            {
                "id": "R6", "categoria": "desempenho",
                "se": {"hd_ruido"},
                "entao": "Falha mecânica iminente do disco rígido.",
                "acao": "Faça backup IMEDIATAMENTE e evite usar o computador "
                        "até a troca do disco.",
                "tecnico": True,
            },
            {
                "id": "R8", "categoria": "desempenho",
                "se": {"lento", "popups"},
                "entao": "Infecção por malware/vírus.",
                "acao": "Execute uma verificação completa com o antivírus "
                        "(ex.: Microsoft Defender) e remova programas desconhecidos.",
                "tecnico": False,
            },
            # Categoria: temperatura
            {
                "id": "R3", "categoria": "temperatura",
                "se": {"desliga_sozinho", "gabinete_quente"},
                "entao": "Superaquecimento (dissipação de calor comprometida).",
                "acao": "Garanta que as saídas de ar não estejam obstruídas e "
                        "verifique se os coolers giram.",
                "tecnico": True,
            },
            {
                "id": "R10", "categoria": "temperatura",
                "se": {"reinicia_sozinho", "poeira_coolers"},
                "entao": "Superaquecimento por acúmulo de poeira.",
                "acao": "Com o computador desligado e fora da tomada, limpe os "
                        "coolers com pincel macio ou ar comprimido.",
                "tecnico": False,
            },
            # Categoria: tela
            {
                "id": "R5", "categoria": "tela",
                "se": {"tela_azul_frequente"},
                "entao": "Driver de dispositivo corrompido ou incompatível.",
                "acao": "Anote o código de erro da tela azul e atualize os "
                        "drivers pelo Windows Update ou Gerenciador de Dispositivos.",
                "tecnico": False,
            },
            {
                "id": "R9a", "categoria": "tela",
                "se": {"artefatos_tela"},
                "entao": "Placa de vídeo (GPU) com defeito.",
                "acao": "Atualize o driver de vídeo. Persistindo, a placa de "
                        "vídeo deve ser testada.",
                "tecnico": True,
            },
            {
                "id": "R9b", "categoria": "tela",
                "se": {"trava_jogos_videos"},
                "entao": "Placa de vídeo (GPU) com defeito.",
                "acao": "Atualize o driver de vídeo. Persistindo, a placa de "
                        "vídeo deve ser testada.",
                "tecnico": True,
            },
            # Categoria: rede
            {
                "id": "R7", "categoria": "rede",
                "se": {"sem_internet", "outros_dispositivos_conectam"},
                "entao": "Problema na placa ou no driver de rede.",
                "acao": "Reinicie o computador, execute a Solução de Problemas "
                        "de Rede do Windows e atualize o driver de rede.",
                "tecnico": False,
            },
        ]

    def validar_base(self):
        """Verifica se toda condição usada nas regras tem uma pergunta.
        Protege contra erro de digitação no nome ("disco_10" -> "disco_100")
        """
        erros = []
        for regra in self.regras:
            if regra["categoria"] not in self.categorias:
                erros.append(f"{regra['id']}: categoria '{regra['categoria']}' não existe.")
            for fato in regra["se"]:
                if fato not in self.perguntas:
                    erros.append(f"{regra['id']}: fato '{fato}' não tem pergunta cadastrada.")
        return erros

    def perguntas_da_categoria(self, categoria):
        """Gera a lista de perguntas da categoria a partir das REGRAS.
        Um fato usado por várias regras ("lento" em R4 e R8) é perguntado 1 vez só.
        """
        # 1. Junta (união) os fatos das regras da categoria. Como é set, os repetidos somem sozinhos
        necessarios = set()
        for regra in self.regras:
            if regra["categoria"] == categoria:
                necessarios = necessarios.union(regra["se"])

        # 2. Devolve na ordem de self.perguntas, porque set ñ garante ordem
        return [fato for fato in self.perguntas if fato in necessarios]

    # MOTOR DE INFERÊNCIA (encadeamento para frente)
    def inferir(self, fatos):
        """Devolve as regras que têm TODAS as condições entre os fatos."""
        # issubset -> "todas as condições da regra estão nos fatos?" Fatos a mais ñ atrapalham
        # Checar: Unidade-2_e_3.pdf, slide 38, linha 20
        disparadas = []
        for regra in self.regras:
            if regra["se"].issubset(fatos):
                disparadas.append(regra)
        return disparadas

    # MÓDULO DE EXPLICAÇÃO
    def explicar(self, regra):
        """Monta o texto que mostra POR QUE a regra disparou.
        É isso que diferencia um SE de um questionário comum.
        """
        linhas = [f"Regra {regra['id']} disparou porque você respondeu:"]
        # Percorre na mesma ordem em que as perguntas foram feitas
        for fato, texto in self.perguntas.items():
            if fato in regra["se"]:
                linhas.append(f"   - {texto} -> Sim")
        linhas.append(f"   ENTÃO: {regra['entao']}")
        return "\n".join(linhas)


# INTERFACE (TERMINAL)
def perguntar_sim_nao(texto):
    """Faz uma pergunta e só aceita 's' ou 'n'. Retorna True para sim."""
    # while True -> ñ sabemos quantas vezes o usuário vai digitar algo inválido
    while True:
        resposta = input(f"{texto} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("   Resposta inválida. Digite 's' para sim ou 'n' para não.")


def escolher_categoria(se):
    """Mostra o menu de categorias e devolve a escolhida (None = sair)."""
    chaves = list(se.categorias)  # lista para acessar por número
    print("\nQual é o tipo de problema?")
    for numero, chave in enumerate(chaves, start=1):
        print(f"  {numero} - {se.categorias[chave]}")
    print("  0 - Sair")

    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return None
        # isdigit() evita erro no int() quando o usuário digita texto ("abc")
        if opcao.isdigit() and 1 <= int(opcao) <= len(chaves):
            return chaves[int(opcao) - 1]
        print("   Opção inválida.")


def coletar_fatos(se, categoria):
    """Faz as perguntas da categoria e monta a MEMÓRIA DE TRABALHO."""
    # Só guarda os "sim", igual aos sintomas dos pacientes no slide 38
    fatos = set()
    print()
    for fato in se.perguntas_da_categoria(categoria):
        if perguntar_sim_nao(se.perguntas[fato]):
            fatos.add(fato)
    return fatos


def mostrar_resultado(se, disparadas):
    """Exibe diagnóstico, ação, aviso de técnico e oferece a explicação."""
    print("\n" + "=" * 60)

    # R11: nenhuma regra disparou
    if not disparadas:
        print("DIAGNÓSTICO INCONCLUSIVO (R11)")
        print("Nenhuma regra da base de conhecimento corresponde aos sintomas.")
        print("[!] Encaminhe o caso a um técnico especializado.")
        print("=" * 60)
        return

    # Agrupa regras com o msm diagnóstico para ñ mostrar 2x
    # chave = diagnóstico | valor = lista de regras que chegaram nele
    diagnosticos = {}
    for regra in disparadas:
        if regra["entao"] not in diagnosticos:
            diagnosticos[regra["entao"]] = []
        diagnosticos[regra["entao"]].append(regra)

    for numero, (diagnostico, regras) in enumerate(diagnosticos.items(), start=1):
        principal = regras[0]  # regras do mesmo grupo têm a mesma ação
        print(f"DIAGNÓSTICO {numero}: {diagnostico}")
        print(f"Ação recomendada: {principal['acao']}")
        if principal["tecnico"]:
            print("[!] Recomenda-se procurar assistência técnica.")
        print("-" * 60)

    if perguntar_sim_nao("Deseja ver por que o sistema chegou a essa conclusão?"):
        for regra in disparadas:
            print()
            print(se.explicar(regra))
    print("=" * 60)


def main():
    se = SistemaEspecialista()

    # Verifica a base antes de usar o sistema
    erros = se.validar_base()
    if erros:
        print("Erro na base de conhecimento:")
        for erro in erros:
            print(" -", erro)
        return

    print("=" * 60)
    print("PCDoctor - Diagnóstico de Problemas em Computadores")
    print("Responda às perguntas com 's' (sim) ou 'n' (não).")
    print("=" * 60)

    while True:
        categoria = escolher_categoria(se)
        if categoria is None:
            break
        fatos = coletar_fatos(se, categoria)  # memória de trabalho
        disparadas = se.inferir(fatos)        # motor de inferência
        mostrar_resultado(se, disparadas)     # resultado + explicação
        if not perguntar_sim_nao("\nDeseja fazer um novo diagnóstico?"):
            break

    print("\nObrigado por usar o PCDoctor!")


# Só executa main() quando o arquivo é rodado direto (python pcdoctor.py), ñ quando é importado
if __name__ == "__main__":
    main()