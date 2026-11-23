# RETOMAR · WT.AG Cases [A]MANHÃ

Instruções para um Claude (ou uma pessoa) retomar este projeto do zero. Leia
inteiro antes de mexer.

## O que é

Apresentação em HTML **só com cases da WT.AG**, recortada das Credenciais v2.
Palco fixo 1920×1080, sem build, sem framework. Cada case é uma tela (`<section>`)
com fundo desfocado, logo do cliente + "apresenta", selo da campanha, texto
(Contexto / Insight / Ideia), mídia (vídeo + miniaturas) e, quando há, números e
faixa de repercussão.

Publicada no GitHub Pages: **https://wtag.github.io/wtag-cases/**
Cada **opção** (versão com cases e ordem próprias) tem link: `…/wtag-cases/?opcao=NN`.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| **Projeto vivo** (é daqui que sai o link) | Mac: `~/Projetos/wtag-cases` · repositório git `github.com/wtag/wtag-cases`, branch `main` |
| Material bruto dos cases (PNG, MOV, PSB, docx) | `~/Projetos/wtag-cases/cases/` (fora do git, no `.gitignore`) |
| Pasta do Drive do projeto | `Drives compartilhados/WT.AG/2026/Criação/WTA_CasesAmanhaCredenciais/` |
| PDFs e links de cada opção | `…/WTA_CasesAmanhaCredenciais/Opcoes/Opcao-NN_*/` |
| Backup do projeto (cópia, sem .git e sem `cases/`) | `…/WTA_CasesAmanhaCredenciais/_Backup-Projeto/wtag-cases/` |
| Projetos irmãos (só leitura, NÃO mexer) | `~/Projetos/wtag-credenciais-2026`, `wtag-credenciais-v2`, `wtag-concorrencia-2026` |
| Imagens/logos/selos de todos os cases antigos + `_base.pdf` de cada | `~/Desktop/_LegadoCredenciais/<Cliente-Campanha>/` |

**O backup no Drive é só cópia.** Editar lá não muda o link. Se o Mac não tiver o
projeto, recupere do GitHub (`git clone https://github.com/wtag/wtag-cases.git`)
ou copie `_Backup-Projeto/wtag-cases` de volta para `~/Projetos/` (aí refaça o
`git init` ligado ao remoto).

## Arquivos que importam

```
index.html      tudo: as telas (<section>) e, NO TOPO, as listas de controle
css/deck.css    visual do deck (inclui os arranjos de mídia, ver abaixo)
css/pdf.css     ajustes para imprimir em PDF
js/cases.js     aplica window.CASES / window.CAPAS / window.OPCOES (roda antes do deck.js)
js/deck.js      navegação, animações, contadores, sumário (ATOS = nome de cada cliente)
js/i18n-dic.js  dicionário PT→EN (botão PT/EN); chave = texto exato do index.html
gerar-pdf.py    PDF de uma opção
servidor.py     servidor local (precisa dele para vídeo no Safari)
assets/img/cases/        fundo, hero (pôster), vidN/imgN (miniaturas), fullN (ampliar); -m = versão leve
assets/img/logos-cases/  logo do cliente (negativo) e selos da campanha (PNG recortado na tinta)
assets/video/            vídeos comprimidos (H.264, faststart)
```

## As listas no topo do index.html

1. **`window.CASES`**: `true`/`false` por case. Só vale se `OPCAO_PADRAO` estiver vazia.
2. **`window.CAPAS`**: `false` = nenhuma capa de cliente aparece (decisão atual).
3. **`window.OPCAO_PADRAO`**: a opção que o link **sem** `?opcao=` mostra.
   **Hoje: `'02'` (novembro).** Para pôr outra versão no ar no link principal,
   é só trocar este número.
4. **`window.OPCOES`**: cada opção tem `nome`, `capas` e `casos` (lista de ids na
   ORDEM em que entram). A opção pode trazer case que está `false` em CASES.

Opções atuais:

| Opção | Cases (nesta ordem) | Pasta no Drive |
|---|---|---|
| 01 | Odontoprev Dia dos Pais · Odontoprev 39 Anos · BarraShoppingSul Now New Barra! · Keeta Crias do Corre | `Opcao-01_Odontoprev-Barra-Keeta` |
| 02 (novembro) · **no link principal** | ParkShopping Canoas Natal não dá pra adiar · Calvin Klein Cinemas BTS · Sicredi Clubinho da Poupança · Odontoprev Rir é o Melhor Tempero | `Opcao-02_Novembro_ParkShopping-CalvinKlein-Clubinho` |

Ids de todos os cases que existem no arquivo: `s-odontoprev-pais`,
`s-odontoprev-aniversario`, `s-odontoprev-tempero`, `s-barrashoppingsul`, `s-keeta-crias-do-corre`,
`s-parkshopping`, `s-ck-cinemas`, `s-sicredi`, `s-bichinhos` (Clubinho),
`s-private`, `s-horoscopo`, `s-magalu`, `s-lojinha-fiuk`, `s-central-corre`,
`s-pulando-bloco`, `s-keeta-brasil-corre`, `s-bridgestone`, `s-golden-lake`.

## Tarefas comuns

### Rodar localmente
```bash
cd ~/Projetos/wtag-cases && python3 servidor.py 8768    # http://localhost:8768/?opcao=02
```
Teclas: ←/→ navegam, número vai para a tela, espaço abre o sumário.

### Criar uma opção nova
1. Acrescentar o bloco em `window.OPCOES` (copiar um existente, trocar número,
   nome, `capas` e a lista `casos`).
2. Conferir no navegador `?opcao=NN`.
3. Criar a pasta `Opcoes/Opcao-NN_<Descrição>` no Drive (copiar `_Modelo-Opcao`),
   preencher o `LEIA-ME.txt` e gerar o PDF:
   ```bash
   python3 gerar-pdf.py NN --saida "<pasta da opção no Drive>"
   ```
4. Commit e avisar para dar **Push origin** no GitHub Desktop.

### Adicionar um case novo (padrão usado até aqui)
A pasta do case chega em `cases/<Mês>/<Cliente - Campanha>/` com: textos (docx ou
Google Doc), `Logo` (versão branca), `Selo`/Lettering, `Foto_fundo`/`Fundo`,
`Video_Principal`/`Imagem principal`, vídeos e fotos de complemento. Notas em
`.textClipping` trazem pedidos específicos (leia com `strings`/`plutil`).
1. **Textos**: Contexto/Insight/Ideia. O `<p>` mostra uma versão curta (~170
   caracteres, 4 linhas); o texto completo vai literal em `data-texto` (abre no
   "+ Texto completo"). Não inventar número nem texto.
2. **Imagens** (Pillow, recorte centrado no rosto; o detector de rostos/texto do
   macOS está em `~/Projetos/wtag-arp-2026/plugin/skills/onepage-arp-wtag/scripts/focos.swift`):
   - fundo 1920×1080 + `-m` 1152×648
   - hero 16:9: 1920×1080 (ou no aspecto da caixa) + `-m`; hero vertical 956×1740
   - miniaturas 640×449 + `-m` 384×270 (caixa 312×219 no deck sem repercussão)
   - ampliar (`data-full`): lado maior 1600
   - selo: recortar na tinta, altura 480 + `-m` 288; logo: recortado, ~110 de altura
3. **Vídeos** (ffmpeg): principal 1920/1500k; secundários e verticais
   1280/1000–1200k; sempre `-movflags +faststart`. Arquivo > 100 MB não sobe no GitHub.
4. **Acento** (`--acento`): amostrar do selo, não escolher. Precisa contraste no escuro.
5. Colar a `<section>` (copiar uma parecida), id `s-<nome>`, `data-ato="<cliente>"`;
   acrescentar o id em `window.CASES` (e na opção); se cliente novo, nome em
   `ATOS` no `js/deck.js`; traduções no `js/i18n-dic.js`.
6. Subir `?v=N` de css/js no `index.html` (cache):
   `sed -i '' 's/?v=9"/?v=10"/g' index.html` (ver o número atual antes).

### Arranjos de mídia (classes na `<section>`)
| Classe | Uso |
|---|---|
| `case--sem-reperc` | sem faixa de repercussão: mídia e números vão até 870 de altura |
| `case--sem-kpis` | sem números |
| `case--vert` | campanha só 9:16: reel grande + grade 2×2 |
| `case--vert1` | 1 filme 9:16 na altura toda + 3 fotos empilhadas (Odontoprev, os três) |
| `case--vert2` | 2 filmes 9:16 lado a lado (Calvin Klein) |
| `case--vert3` | 3 filmes 9:16 lado a lado |
| `case__video--still` | destaque é foto, não vídeo (ParkShopping) |

### Publicar
O Claude faz o commit; **o push é pelo GitHub Desktop** (Push origin): o
terminal não tem o login do GitHub. Depois de 1–2 min o link atualiza (Cmd+Shift+R).

### Backup no Drive
```bash
D="$HOME/Library/CloudStorage/GoogleDrive-bernardo@wt.ag/Drives compartilhados/WT.AG/2026/Criação/WTA_CasesAmanhaCredenciais"
rsync -a --delete --exclude .git --exclude .claude --exclude /cases --exclude '_teste-*' \
  --exclude .DS_Store --exclude __pycache__ ~/Projetos/wtag-cases/ "$D/_Backup-Projeto/wtag-cases/"
```
Nunca colocar a pasta `.git` no Drive (o Drive corrompe o repositório).

## Decisões já tomadas (não refazer sem pedir)

- Topo das telas: **"[A]MANHÃ"** no lugar de "Credenciais"; canto direito "2026".
- Fecho: **"MARCAS PROTAGONISTAS DA CULTURA?"** (EN: "BRANDS THAT LEAD CULTURE?").
- Sem capas de cliente (`CAPAS = false`).
- **BarraShoppingSul**: usar a one-page ANTIGA das credenciais (texto, 6 números,
  vídeos e selo SVG originais). O material novo de `cases/Barra - New Barra` foi
  descartado a pedido.
- **Odontoprev 39 Anos**: a "Ideia" do doc era cópia da do Dia dos Pais; vale o
  parágrafo "A entrega consistiu em 4 filmes…".
- **Calvin Klein**: sem selo e sem "apresenta" (logo CK grande); texto inteiro na
  tela, corpo 18,5px, terminando na base dos filmes; fundo reenquadrado para o JK
  aparecer à esquerda; acento creme (marca P&B).
- **ParkShopping**: destaque é a "Imagem principal" (foto); os 3 episódios tocam
  nas miniaturas. As miniaturas são as capas `thumb_1..3` (9:16) recortadas na
  faixa do título; a capa vertical inteira (`parkshopping-capaN.jpg`) é o pôster
  do vídeo em tela cheia. "Imagem extra 1/2" e "Foto conteúdo 1/2" ficaram de fora.
- Texto de comentário HTML sem `<!--` vaza para a tela: ao editar comentários,
  conferir que abrem e fecham.

## Pendências conhecidas

- **Keeta Crias do Corre**: o lettering é PROVISÓRIO (recortado por cor do `.psb`).
  Trocar `assets/img/logos-cases/selo-crias-do-corre(-m).png` pelo PNG transparente
  oficial quando chegar.
- **ParkShopping**: números de campanha recém-lançada (orgânico Meta, até 16/11).
  Atualizar perto do envio.
- **Clubinho da Poupança**: ganhou coluna de números em 18.11.2026 (669 contas,
  +R$3M movimentação, 748 pelúcias, +2M impressões na landing page).
- **Odontoprev Rir é o Melhor Tempero** (entrou em 23.11.2026, opção 02): sem
  números, porque as publicações ainda não foram ao ar; no lugar, bloco
  "Resultado" com o texto do doc. Quando os números chegarem, tirar
  `case--sem-kpis` e pôr a coluna `case__kpis--vert` (ver Odontoprev 39 Anos).
- **Odontoprev Dia dos Pais**: o doc diz "Fado do Dente" (mantido como está).
- Commits locais podem estar aguardando **Push origin** no GitHub Desktop:
  conferir com `git status -sb` (mostra `ahead N`).

## Projeto relacionado

One-pages em PDF para o **Salão ARP 2026** usam este mesmo visual, mas vivem em
outro projeto: `~/Projetos/wtag-arp-2026`, com a skill publicada para o time
(`wtag-onepage-arp`, plugin na biblioteca da organização no claude.ai).
