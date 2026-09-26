class SistemaEspecialista:
    """Gerencia a base de conhecimento, regras de inferência e explicações."""

    def __init__(self):
        # Categorias para filtrar perguntas com base no tipo de problema
        self.categorias = {
            "energia": "Não liga / tela preta",
            "desempenho": "Lentidão / ruídos no disco",
            "temperatura": "Desliga ou reinicia sozinho",
            "tela": "Tela azul / defeitos na imagem",
            "rede": "Sem internet",
        }

        # Base de fatos e perguntas correspondentes (respostas sim/não)
        self.perguntas = {
            # Energia
            "sem_energia": "Ao apertar o botão, o computador fica totalmente sem sinal (nenhuma luz, som ou ventoinha)?",
            "pc_liga": "O computador liga ao apertar o botão (ventoinhas giram)?",
            "emite_bips": "O computador emite bipes ao ligar?",
            "tela_preta": "A tela permanece preta depois de ligar?",
            # Desempenho
            "lento": "O computador está lento no uso geral?",
            "disco_100": "No Gerenciador de Tarefas, o uso do disco fica próximo de 100%?",
            "hd_ruido": "O HD faz ruídos anormais (cliques, arranhados)?",
            "popups": "Aparecem pop-ups ou anúncios inesperados?",
            # Temperatura
            "desliga_sozinho": "O computador desliga sozinho?",
            "gabinete_quente": "O gabinete fica muito quente ao toque?",
            "reinicia_sozinho": "O computador reinicia sozinho, aleatoriamente?",
            "poeira_coolers": "Há acúmulo visível de poeira nos coolers?",
            # Tela
            "tela_azul_frequente": "Ocorrem telas azuis (BSOD) com frequência?",
            "artefatos_tela": "Aparecem artefatos na tela (riscos, quadrados, cores estranhas)?",
            "trava_jogos_videos": "O computador trava durante jogos ou vídeos?",
            # Rede
            "sem_internet": "O computador está sem conexão com a internet?",
            "outros_dispositivos_conectam": "Outros dispositivos da mesma rede conectam normalmente?",
        }

        # Base de Regras (SE-ENTÃO)
        self.regras = [
            # Categoria: Energia
            {
                "id": "R1", "categoria": "energia",
                "se": {"sem_energia"},
                "entao": "Fonte de alimentação defeituosa.",
                "acao": "Teste em outra tomada e com outro cabo de energia. Persistindo, substitua a fonte.",
                "tecnico": True,
            },
            {
                "id": "R2a", "categoria": "energia",
                "se": {"pc_liga", "emite_bips"},
                "entao": "Memória RAM com defeito.",
                "acao": "Com o PC desligado e fora da tomada, retire e reencaixe os pentes de memória.",
                "tecnico": True,
            },
            {
                "id": "R2b", "categoria": "energia",
                "se": {"pc_liga", "tela_preta"},
                "entao": "Memória RAM com defeito.",
                "acao": "Com o PC desligado e fora da tomada, retire e reencaixe os pentes de memória.",
                "tecnico": True,
            },
            # Categoria: Desempenho
            {
                "id": "R4", "categoria": "desempenho",
                "se": {"lento", "disco_100"},
                "entao": "Disco rígido (HD) ou SSD com falha.",
                "acao": "Faça backup dos arquivos importantes e verifique a saúde do disco com ferramenta de diagnóstico.",
                "tecnico": True,
            },
            {
                "id": "R6", "categoria": "desempenho",
                "se": {"hd_ruido"},
                "entao": "Falha mecânica iminente do disco rígido.",
                "acao": "Faça backup IMEDIATAMENTE e evite usar o computador até a substituição do disco.",
                "tecnico": True,
            },
            {
                "id": "R8", "categoria": "desempenho",
                "se": {"lento", "popups"},
                "entao": "Infecção por malware/vírus.",
                "acao": "Execute uma verificação completa com o antivírus e remova programas desconhecidos.",
                "tecnico": False,
            },
            # Categoria: Temperatura
            {
                "id": "R3", "categoria": "temperatura",
                "se": {"desliga_sozinho", "gabinete_quente"},
                "entao": "Superaquecimento (dissipação de calor comprometida).",
                "acao": "Certifique-se de que as saídas de ar não estão obstruídas e verifique se os coolers giram.",
                "tecnico": True,
            },
            {
                "id": "R10", "categoria": "temperatura",
                "se": {"reinicia_sozinho", "poeira_coolers"},
                "entao": "Superaquecimento por acúmulo de poeira.",
                "acao": "Com o PC desligado e fora da tomada, limpe os coolers com pincel macio ou ar comprimido.",
                "tecnico": False,
            },
            # Categoria: Tela
            {
                "id": "R5", "categoria": "tela",
                "se": {"tela_azul_frequente"},
                "entao": "Driver de dispositivo corrompido ou incompatível.",
                "acao": "Anote o código de erro da tela azul e atualize os drivers.",
                "tecnico": False,
            },
            {
                "id": "R9a", "categoria": "tela",
                "se": {"artefatos_tela"},
                "entao": "Placa de vídeo (GPU) com defeito.",
                "acao": "Atualize o driver de vídeo. Persistindo, teste a placa de vídeo.",
                "tecnico": True,
            },
            {
                "id": "R9b", "categoria": "tela",
                "se": {"trava_jogos_videos"},
                "entao": "Placa de vídeo (GPU) com defeito.",
                "acao": "Atualize o driver de vídeo. Persistindo, teste a placa de vídeo.",
                "tecnico": True,
            },
            # Categoria: Rede
            {
                "id": "R7", "categoria": "rede",
                "se": {"sem_internet", "outros_dispositivos_conectam"},
                "entao": "Problema na placa ou no driver de rede.",
                "acao": "Reinicie o computador, execute a solução de problemas de rede do Windows e atualize o driver.",
                "tecnico": False,
            },
        ]

    def validar_base(self):
        """Verifica consistência da base de conhecimento (fatos e categorias válidos nas regras)."""
        erros = []
        for regra in self.regras:
            if regra["categoria"] not in self.categorias:
                erros.append(f"Regra {regra['id']}: categoria '{regra['categoria']}' não existe.")
            for fato in regra["se"]:
                if fato not in self.perguntas:
                    erros.append(f"Regra {regra['id']}: fato '{fato}' não possui pergunta cadastrada.")
        return erros

    def perguntas_da_categoria(self, categoria):
        """Retorna perguntas únicas associadas às regras de uma categoria."""
        necessarios = set()
        for regra in self.regras:
            if regra["categoria"] == categoria:
                necessarios.update(regra["se"])
        return [fato for fato in self.perguntas if fato in necessarios]

    def inferir(self, fatos):
        """Motor de inferência (encadeamento para frente): retorna regras cujas premissas estão contidas nos fatos."""
        return [regra for regra in self.regras if regra["se"].issubset(fatos)]

    def explicar(self, regra):
        """Gera o rastreamento justificando o disparo da regra."""
        linhas = [f"Regra {regra['id']} disparada pelas respostas:"]
        for fato, texto in self.perguntas.items():
            if fato in regra["se"]:
                linhas.append(f"   - {texto} -> Sim")
        linhas.append(f"   ENTÃO: {regra['entao']}")
        return "\n".join(linhas)


def perguntar_sim_nao(texto):
    """Obtém e valida uma resposta booleana (sim/não) do usuário."""
    while True:
        resposta = input(f"{texto} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("   Resposta inválida. Digite 's' para sim ou 'n' para não.")


def escolher_categoria(sistema):
    """Exibe o menu de categorias e retorna a opção escolhida pelo usuário."""
    chaves = list(sistema.categorias.keys())
    print("\nQual é o tipo de problema?")
    for i, chave in enumerate(chaves, start=1):
        print(f"  {i} - {sistema.categorias[chave]}")
    print("  0 - Sair")

    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return None
        if opcao.isdigit() and 1 <= int(opcao) <= len(chaves):
            return chaves[int(opcao) - 1]
        print("   Opção inválida.")


def coletar_fatos(sistema, categoria):
    """Coleta os fatos (sintomas) respondidos positivamente pelo usuário."""
    fatos = set()
    print()
    for fato in sistema.perguntas_da_categoria(categoria):
        if perguntar_sim_nao(sistema.perguntas[fato]):
            fatos.add(fato)
    return fatos


def mostrar_resultado(sistema, disparadas):
    """Exibe diagnósticos, ações recomendadas e oferece explicações detalhadas."""
    print("\n" + "=" * 60)

    if not disparadas:
        print("DIAGNÓSTICO INCONCLUSIVO")
        print("Nenhuma regra da base de conhecimento corresponde aos sintomas.")
        print("[!] Recomenda-se encaminhar o caso a um técnico especializado.")
        print("=" * 60)
        return

    # Agrupa regras por diagnóstico para evitar duplicações
    diagnosticos = {}
    for regra in disparadas:
        diagnosticos.setdefault(regra["entao"], []).append(regra)

    for i, (diagnostico, regras) in enumerate(diagnosticos.items(), start=1):
        principal = regras[0]
        print(f"DIAGNÓSTICO {i}: {diagnostico}")
        print(f"Ação recomendada: {principal['acao']}")
        if principal["tecnico"]:
            print("[!] Assistência técnica recomendada.")
        print("-" * 60)

    if perguntar_sim_nao("Deseja ver a explicação de como o sistema chegou a essa conclusão?"):
        for regra in disparadas:
            print(f"\n{sistema.explicar(regra)}")
    print("=" * 60)


def main():
    sistema = SistemaEspecialista()

    # Validação prévia da base de conhecimento
    erros = sistema.validar_base()
    if erros:
        print("Erro na base de conhecimento:")
        for erro in erros:
            print(f" - {erro}")
        return

    print("=" * 60)
    print("PCDoctor - Diagnóstico de Problemas em Computadores")
    print("Responda às perguntas com 's' (sim) ou 'n' (não).")
    print("=" * 60)

    while True:
        categoria = escolher_categoria(sistema)
        if categoria is None:
            break
        fatos = coletar_fatos(sistema, categoria)
        disparadas = sistema.inferir(fatos)
        mostrar_resultado(sistema, disparadas)

        if not perguntar_sim_nao("\nDeseja realizar um novo diagnóstico?"):
            break

    print("\nObrigado por usar o PCDoctor!")


if __name__ == "__main__":
    main()
        
