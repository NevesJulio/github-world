# github-world

Bem vindo ao mapa em pixel art que representa os principais repositórios do GitHub como ilhas, atualizado automaticamente por cron no GitHub Actions. Cada ilha usa a árvore real de arquivos para formar uma colônia de módulos hexagonais conectados, com crescimento orgânico.

![Mundo dos repositórios](world.gif)

## Executar

Requer Python 3.11 ou superior.

```bash
python3 -m pip install -r requirements.txt
python3 generate.py
```

Por padrão, consulta apenas o repositório público mais recentemente atualizado de `NevesJulio`, sem forks. Para outro usuário:

```bash
python3 generate.py --username SEU_USUARIO
```

Para escolher diretamente um repositório público:

```bash
python3 generate.py --username SEU_USUARIO --repo NOME_DO_REPOSITORIO
```

Para voltar a mostrar dois ou três repositórios, use `--limit 2` ou `--limit 3`. Alterar o valor padrão de `get_top_repositories()` 
A variável opcional `GITHUB_TOKEN` autentica as consultas e aumenta o limite de requests. O token nunca é salvo no snapshot. O workflow usa o token disponibilizado pelo GitHub Actions e atualiza `map.png` e `world.gif` a cada seis horas.

Os caminhos dos assets são relativos aos arquivos Python: o gerador também funciona quando executado de outro diretório. As saídas vão para a raiz do projeto por padrão; use `--output-dir /tmp/meu-mapa` para escolher outro destino.

## Executar sem rede ou sandbox com acesso ao GitHub

```bash
python3 generate.py --offline --output-dir /tmp/meu-mapa
```

Esse modo representa a árvore local deste projeto em uma ilha. Diretórios de ferramentas, caches e dependências instaladas são ignorados. A linguagem é identificada como Python para este projeto; atividade e tempo sem atualização ficam desconhecidos, sem métricas simuladas.

Para salvar dados reais e repetir exatamente a mesma geração sem novas consultas:

```bash
python3 generate.py --save-data /tmp/repos.json
python3 generate.py --data /tmp/repos.json --output-dir /tmp/meu-mapa
```

O JSON contém uma lista de repositórios com `name`, `tree` (entradas com `path` e `type`), `main_language`, `languages` (bytes por linguagem), `topics`, `recent_commits`, `pushed_at`, `as_of` e o ícone opcional em `icon_base64`. O layout e a decoração são determinísticos para os mesmos dados e assets, usando uma semente por nome de repositório e frames ordenados.

## Ícone do repositório

O GIF mostra um painel no canto superior esquerdo com o nome e o ícone do repositório. Para definir o ícone, coloque um PNG na raiz do próprio repositório usando exatamente o nome do projeto. Por exemplo:

```text
github-world/github-world.png
```

O nome diferencia maiúsculas de minúsculas. A coleta encontra esse arquivo na árvore da branch padrão e baixa seu conteúdo pela API do GitHub. No modo `--offline`, o gerador procura o mesmo arquivo na raiz local. Imagens retangulares mantêm sua proporção e são centralizadas; se o arquivo não existir ou for inválido, aparece um círculo com a inicial do repositório.

## Significado visual

| Dados | Representação |
| --- | --- |
| Repositório | Uma ilha com nome e contagem de arquivos/diretórios |
| Diretórios principais e arquivos da raiz | Até três construções identificadas por rótulos |
| Arquivos por diretório | Variante 1 abaixo de 20 arquivos, 2 de 20 a 79, 3 a partir de 80 |
| Quantidade de bairros | Novos módulos de casas anexados a um dos seis lados livres |
| Profundidade dos arquivos | Mais folhagem no jardim, limitada a três elementos adicionais |
| Python, R, Julia, Jupyter Notebook | Casas verdes |
| C, C++, Rust, Go, Java | Casas cinza |
| Outras linguagens ou linguagem desconhecida | Casas laranja |
| Linguagens secundárias | Cores das construções auxiliares |
| Commits nos últimos 30 dias | Caixas e barris, até oito elementos |
| Mais de 90 dias sem push | Fonte vazia e mais árvores |
| Push há até 90 dias | Fonte cheia |
| Testes identificados pelo caminho/nome | Cercas na praça |
| README ou diretórios de documentação | Placa na praça |
| Manifestos de dependências | Depósito ou caixa na praça |
| Arquivos, diretórios, testes e documentação | Mistura de árvores definida pelas regras de `world.yaml` |

## Controlar as árvores

A mistura de árvores fica em `world.yaml`. Os quatro grupos correspondem diretamente aos sprites:

| Grupo YAML | Assets | Aparência |
| --- | --- | --- |
| `large` | `t1`, `t2` | Árvores grandes |
| `small` | `t3`, `t4` | Árvores pequenas |
| `large_stump` | `t5`, `t6` | Tocos grandes |
| `small_stump` | `t7`, `t8` | Tocos pequenos |

`defaults` define a mistura mínima. As entradas de `rules` são aplicadas em ordem quando métricas como `min_files`, `min_directories`, `min_depth`, `has_tests` e `has_docs` combinam com o perfil. Por fim, `repositories.NOME.trees` substitui quantidades para um projeto específico. Exemplo:

```yaml
repositories:
  github-world:
    trees:
      large: 1
      small: 2
      large_stump: 1
      small_stump: 2
```

As quantidades ficam fixas pelo YAML. Para cada item, o gerador escolhe de forma determinística uma das duas variantes e procura aleatoriamente uma posição válida no jardim. Isso cria variedade sem perder o controle da composição. A API fornece as métricas usadas pelas regras; ela não precisa reescrever o YAML. Depois de editar, use `python3 generate.py --offline` para conferir rapidamente.

As flores usam os tiles `(3,3)`, `(4,3)` e `(5,3)` de `assets/grama.png`, registrados como `flower1`, `flower2` e `flower3`. A quantidade é controlada separadamente pela densidade:

```yaml
flowers:
  assets: [flower1, flower2, flower3]
  default_density: 5

  repositories:
    github-world:
      density: 12
```

`default_density` é a quantidade padrão. `rules` pode alterar esse valor usando as mesmas condições das árvores, e `repositories.NOME.density` define a quantidade exata para um repositório. A escolha das variantes e posições é aleatória, mas estável para o mesmo nome de projeto.

## Horta

A horta compartilha a honeycomb da praça com o poço. O canteiro usa o asset `h` registrado em `assets.yaml`; a composição repete até três canteiros, monta uma cerca de madeira, posiciona pedras somente no lado externo da cerca e desenha flores numa camada acima dos canteiros. Barris ficam agrupados como um pequeno depósito, enquanto a folhagem adicional completa essa área. A configuração fica em `world.yaml`:

```yaml
farm:
  defaults:
    enabled: true
    beds: 3
    flowers: 6
    extra_rocks: 5
    grass: 8
    barrels: 3

  repositories:
    github-world:
      enabled: true
      beds: 3
      flowers: 7
```

`enabled` adiciona ou remove a horta da praça, `beds` controla de um a três canteiros e `flowers` controla quantas posições recebem flores, até o número de espaços disponível sobre os canteiros. `extra_rocks` e `grass` regulam a densidade da área, enquanto `barrels` aceita de zero a quatro barris organizados. As variantes e posições continuam determinísticas.

Os assets de casas 1 e 2 têm a mesma área de recorte, mas desenhos diferentes; a variante 3 é maior. As métricas orientam escolhas visuais, sem representar uma medida formal de qualidade do projeto. Dependências são contadas por manifestos detectados, sem analisar pacotes individuais.

A coleta usa a árvore da branch padrão, linguagens e até 100 commits dos últimos 30 dias. Essa contagem de commits é limitada a 100. Árvores truncadas ou indisponíveis recebem `*` no nome da ilha; suas contagens são parciais. Falhas nas métricas auxiliares geram avisos e não se tornam atividade zero. Se a listagem principal falhar, o comando termina com erro e orienta usar `--offline` ou um snapshot. Ele não substitui repositórios reais por nomes fictícios.

## Crescimento em honeycomb

Cada repositório usa três hexágonos: uma casa central representa o projeto inteiro, a floresta fica em `(-1, 1)` e o poço com a horta fica em `(1, -1)`. As duas posições são opostas em relação à casa `(0, 0)`, mantendo a construção principal no centro. A decoração considera o nome do repositório e a identidade do módulo, portanto as variações são reproduzíveis.

Cada hexágono tem 16 × 16 tiles, com 20% menos área de terreno que a versão anterior. As casas 1 e 2 mantêm seus sprites; a casa 3 usa uma variante de 10 × 7 tiles, redimensionada com vizinho mais próximo para preservar a nitidez da pixel art. Os recortes originais continuam no catálogo. Os lados compartilhados desaparecem na renderização: a ilha tem terreno contínuo, jardins com tonalidade suave e uma costa em degraus de pixel art. Os caminhos ligam as portas e os módulos, contornam construções e chegam às pontes. O personagem caminha sobre um trecho real desses caminhos.

Aumentar a quantidade total de arquivos pode trocar o tamanho da casa sem alterar as coordenadas dos três módulos. A vegetação da floresta reflete as regras configuradas em `world.yaml`.

O PNG e o GIF têm fundo transparente. No GIF, um índice da paleta é reservado para transparência em todos os frames; o contorno dos rótulos permite lê-los sobre fundos claros ou escuros.

## Organização

- `github_activity.py`: coleta dados brutos da API, com autenticação, paginação e timeout.
- `repo_profile.py`: cria `RepoProfile` e `DirectoryProfile` com identidade e métricas.
- `layout.py`: posiciona ilhas, construções, caminhos e decorações respeitando o tamanho dos sprites.
- `renderer.py`: desenha camadas, etiquetas, pontes e animação do personagem.
- `generate.py`: coordena o processo e fornece as opções de linha de comando.
- `assets.yaml`: catálogo declarativo com spritesheets, recortes, sequências, derivados e grupos.
- `assets.py`: carrega e valida `assets.yaml`, abre as imagens e cria os objetos `Tile`.
- `tiles.py`: classes `Tile` e `AssetManager`.

Os assets ficam em `assets/`. Os frames do personagem ficam em `assets/me/frente`, `assets/me/costas` e `assets/me/lado`; a animação atual usa os frames laterais, ordenados pelo nome do arquivo.

## Adicionar assets

Registre o sprite em `assets.yaml`. `col` e `row` começam em zero; `width` e `height` são medidos em tiles de 16 pixels e valem `1` quando omitidos:

```yaml
tiles:
  minha_placa:
    source: ilhas
    col: 10
    row: 4
    width: 1
    height: 1
```

O nome de `source` precisa existir em `sources`. Para criar uma grade numerada, use `sequences`; os limites de `rows` e `columns` são inclusivos:

```yaml
sequences:
  - prefix: exemplo
    start: 1
    source: ilhas
    rows: [0, 1]
    columns: [2, 4]
```

Esse exemplo cria `exemplo1` até `exemplo6`. `derived` redimensiona um asset existente com vizinho mais próximo, e `groups` reúne nomes usados pela decoração. O carregador rejeita nomes duplicados, fontes ou grupos inexistentes, valores inválidos e recortes fora da imagem.

Os IDs `g`, `e`, `r`, `c`, `f`, `co`, `cc`, `cv`, `p`, `x`, `y` e `m` mantêm o catálogo V2. As árvores antigas usam `t1` a `t8`; os pisos antigos usam `floor1` a `floor10`, a grama antiga `grass1` a `grass8` e as construções de madeira `wood1` a `wood3`. Os nomes próprios evitam substituir os IDs da V2. `path1` é o tile de terra usado nos caminhos. As variantes `co3_compact`, `cc3_compact` e `cv3_compact` são derivadas dos sprites originais para o layout menor.

A origem e a situação das licenças dos sprites estão registradas em [assets/SOURCES.md](assets/SOURCES.md). Ainda faltam os créditos e as licenças originais; não foi atribuída uma licença presumida aos desenhos.

## Validar

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem agrupamento de arquivos, métricas desconhecidas, paginação com forks, limites dos recortes, módulos anexados por lados compartilhados, caminhos conectados, posicionamento sem sobreposição reprodução idêntica dos arquivos PNG/GIF com os mesmos dados e transparência do fundo em todos os frames da animação.
