# PCDoctor — Sistema Especialista para Diagnóstico de Problemas em Computadores

Trabalho da disciplina **Programação de Sistemas Especialistas** — Ciência da Computação, 4º semestre — Universidade Veiga de Almeida (2026).

## Sobre o projeto

O **PCDoctor** auxilia usuários domésticos a identificar a causa provável de falhas em computadores com Windows. O usuário escolhe uma categoria de problema e responde a perguntas de sim ou não sobre os sintomas. Com base em uma base de conhecimento de regras SE–ENTÃO, o sistema infere o diagnóstico mais provável, recomenda uma ação corretiva e explica quais regras levaram à conclusão. Quando o reparo envolve risco, orienta o usuário a procurar assistência técnica.

### Funcionalidades

- Diagnóstico em **5 categorias**: energia, desempenho, temperatura, tela e rede
- Perguntas geradas automaticamente a partir das regras da categoria escolhida
- Diagnóstico com **ação recomendada** e aviso de **assistência técnica**
- **Explicação** do raciocínio: mostra quais regras dispararam e por quê
- Caso **inconclusivo** quando nenhuma regra se aplica
- **Validação da base de conhecimento** ao iniciar o sistema

## Como executar

Requer **Python 3.9+**. Não há bibliotecas externas.

```bash
git clone https://github.com/PedroHammes/ccomp-4s-pse-a1
cd <PASTA_DO_REPOSITORIO> [Entre na pasta onde você baixou]
python pcdoctor.py
```

Responda às perguntas com `s` (sim) ou `n` (não).

### Exemplo de execução

Categoria **2 – Lentidão / ruídos no disco**, respondendo `s`, `s`, `n`, `s`:

```text
DIAGNÓSTICO 1: Disco rígido (HD) ou SSD com falha.
Ação recomendada: Faça backup dos arquivos importantes e verifique a saúde do disco com uma ferramenta de diagnóstico.
[!] Recomenda-se procurar assistência técnica.
------------------------------------------------------------
DIAGNÓSTICO 2: Infecção por malware/vírus.
Ação recomendada: Execute uma verificação completa com o antivírus (ex.: Microsoft Defender) e remova programas desconhecidos.
------------------------------------------------------------
Deseja ver por que o sistema chegou a essa conclusão? (s/n): s

Regra R4 disparou porque você respondeu:
   - O computador está lento no uso geral? -> Sim
   - No Gerenciador de Tarefas, o uso do disco fica próximo de 100%? -> Sim
   ENTÃO: Disco rígido (HD) ou SSD com falha.

Regra R8 disparou porque você respondeu:
   - O computador está lento no uso geral? -> Sim
   - Aparecem pop-ups ou anúncios inesperados? -> Sim
   ENTÃO: Infecção por malware/vírus.
```

## Arquitetura

A estrutura segue a solução em Python apresentada em aula: uma classe `SistemaEspecialista` que concentra a base de conhecimento e o raciocínio, com as condições das regras representadas como conjuntos (`set`).

| Componente do SE | Onde está no código |
|---|---|
| Base de conhecimento | `SistemaEspecialista.__init__` → `categorias`, `perguntas`, `regras` |
| Memória de trabalho | conjunto `fatos`, montado em `coletar_fatos()` |
| Motor de inferência (encadeamento para frente) | `SistemaEspecialista.inferir()` |
| Módulo de explicação | `SistemaEspecialista.explicar()` |
| Validação da base | `SistemaEspecialista.validar_base()` |
| Interface (terminal) | `escolher_categoria()`, `perguntar_sim_nao()`, `mostrar_resultado()`, `main()` |

O motor de inferência testa cada regra com `issubset()`: a regra dispara quando **todos** os fatos da sua condição estão na memória de trabalho.

## Base de regras

| Regra | Categoria | SE | ENTÃO |
|---|---|---|---|
| R1 | Energia | totalmente sem sinal de energia (nenhuma luz, som ou ventoinha) | Fonte de alimentação defeituosa |
| R2a | Energia | liga **E** emite bipes | Memória RAM com defeito |
| R2b | Energia | liga **E** tela permanece preta | Memória RAM com defeito |
| R3 | Temperatura | desliga sozinho **E** gabinete muito quente | Superaquecimento |
| R4 | Desempenho | lento **E** disco próximo de 100% | HD ou SSD com falha |
| R5 | Tela | telas azuis frequentes | Driver corrompido ou incompatível |
| R6 | Desempenho | HD com ruídos anormais | Falha mecânica iminente do HD |
| R7 | Rede | sem internet **E** outros dispositivos conectam | Placa ou driver de rede |
| R8 | Desempenho | lento **E** pop-ups inesperados | Malware/vírus |
| R9a | Tela | artefatos visuais na tela | Placa de vídeo com defeito |
| R9b | Tela | travamentos em jogos ou vídeos | Placa de vídeo com defeito |
| R10 | Temperatura | reinicia sozinho **E** poeira nos coolers | Superaquecimento por poeira |
| R11 | — | nenhuma regra satisfeita | Inconclusivo: encaminhar a um técnico |

### Decisões de modelagem

- **Somente fatos positivos:** a memória de trabalho guarda apenas as respostas "sim", como no exemplo da aula. Condições negativas foram reescritas como um fato positivo (ex.: "não liga e sem luzes nem sons" → `sem_energia`).
- **Condições com OU:** foram divididas em duas regras com a mesma conclusão (R2a/R2b e R9a/R9b), o equivalente a várias cláusulas de um mesmo predicado em Prolog.
- **R11:** não tem condição própria, então não está na lista de regras. Ela é o caso em que nenhuma regra dispara.

## Histórico de desenvolvimento

Cada etapa do código corresponde a um commit que pode ser executado sozinho:

1. Base de conhecimento (categorias, perguntas e regras)
2. Motor de inferência, testado com fatos fixos
3. Interface de perguntas no terminal e memória de trabalho
4. Exibição do resultado e caso inconclusivo (R11)
5. Módulo de explicação
6. Validação da base de conhecimento

## Protótipo de telas

🔗 **[Protótipo no Figma](https://www.figma.com/proto/BiOmMNhyKVqNB483FL7hg7/Sistema-Especialista---PCDoctor?node-id=1-2&p=f&viewport=584%2C343%2C1&t=MwzB0olUUNwFNUdo-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&classId=8c8307dd-ba92-40d5-b65c-71969b69ebb8&assignmentId=865c0561-2a1d-4c17-92ff-139399c151bc&submissionId=9bc39562-8ac1-c208-8e78-2d9b4a1fde05)**

Telas: boas-vindas, seleção de categoria, pergunta, resultado e explicação.
