# WT.AG · Cases

Apresentação **só com os cases** da WT.AG, em link próprio. Foi recortada do
Credenciais v2 (`~/Projetos/wtag-credenciais-v2`) em 07.10.2026 e vive separada:
mexer aqui não muda as credenciais, e mexer lá não muda isto.

Mesmo motor, mesmo visual: palco 1920×1080, sem build. Abra o `index.html` ou
rode o servidor (precisa dele para vídeo no Safari):

```bash
python3 servidor.py 8768      # http://localhost:8768
```

## O que tem

Capa → divisor CASES → cases → fecho.

**No ar nesta versão (07.10.2026):**

| Cliente | Cases |
|---|---|
| Odontoprev | Dia dos Pais (Cuidar é Mágico) · 39 Anos |
| Multiplan | BarraShoppingSul · Now New Barra! |
| Keeta | Crias do Corre |

**No arquivo, ocultos** (voltam trocando `false` por `true`): Sicredi Serrana
(40 Anos, Clubinho da Poupança, Private, Horóscopo do Golpe), Magalu (Craques
Gigantes, Lojinha do Fiuk), Keeta (Central do Corre, Pulando o Bloco, Brasil
Corre), Bridgestone (Seu Pneu de Carro Novo), Multiplan (Golden Lake).

A ordem na tela é a ordem das `<section>` no `index.html`.

## Capas de cliente

`window.CAPAS = false`, logo abaixo da lista de cases, tira todas as capas de
cliente: os cases entram direto depois do divisor. Com `true`, cada capa volta
a aparecer enquanto houver um case daquele cliente no ar. A Odontoprev não tem
capa feita.

## Arranjos de mídia

Os módulos de números e de repercussão são opcionais, por classe na `<section>`:

| Classe | Quando |
|---|---|
| `case--sem-reperc` | sem repercussão: mídia e números descem até onde estaria o rodapé |
| `case--sem-kpis` | sem números: a mídia encosta na margem direita |
| `case--vert` | campanha só em 9:16: um reel grande + quatro em grade |
| `case--vert3` | três filmes 9:16 lado a lado |
| `case--vert1` | um filme 9:16 na altura inteira + três fotos horizontais empilhadas |

## Ocultar e mostrar cases

**1 · No arquivo — muda o link para todo mundo.** No topo do `index.html` está a
lista `window.CASES`. Troque `true` por `false` para tirar um case; `false` por
`true` para trazer de volta. O slide continua no arquivo, só sai da
apresentação, do sumário e do rodapé. A **capa do cliente some sozinha** quando
todos os cases dele estão ocultos.

**2 · No endereço — um recorte por envio, sem republicar.**

| Endereço | Mostra |
|---|---|
| `…/?so=odontoprev` | só os dois da Odontoprev |
| `…/?so=odontoprev&sem=odontoprev-pais` | Odontoprev, menos o Dia dos Pais |
| `…/?sem=keeta` | tudo, menos a Keeta |

Vale o nome do cliente (`odontoprev`, `multiplan`, `keeta`, `sicredi`,
`magalu`, `bridgestone`) ou o id do case sem o `s-` (`odontoprev-pais`,
`odontoprev-aniversario`, `keeta-crias-do-corre`…). O endereço **só estreita**: um case marcado `false` no arquivo
não volta por link.

## Cache

`css/deck.css`, `js/*.js` entram com `?v=NN` no `index.html`. Editou um deles,
suba o número em todas as linhas:

```bash
sed -i '' 's/?v=4"/?v=5"/g' index.html
```

A lista de cases fica **dentro** do `index.html` justamente para não precisar
disso ao ocultar um case.

## Publicar (GitHub Pages)

1. Criar no GitHub, pelo GitHub Desktop, o repositório **vazio** (sem README,
   sem licença) — por exemplo `wtag/wtag-cases`.
2. Apontar e empurrar:

   ```bash
   git remote add origin https://github.com/wtag/wtag-cases.git
   git push -u origin main
   ```

3. **Settings → Pages** · `Deploy from a branch` · `main` · `/ (root)`.

O `.nojekyll` na raiz já está aqui; sem ele o Pages ignora pastas com `_`.

## Trazer um case novo do Credenciais v2

Copie a `<section>` do case (e a capa do cliente, se for cliente novo) para o
`index.html` daqui, troque `data-ato="cases"` pelo nome do cliente, apague a
pílula `Clientes` (aqui não há tela de marcas parceiras), copie os arquivos de
`assets/` que ela usa e acrescente o id na lista `window.CASES`. Se esquecer a
lista, o case aparece mesmo assim e o console do navegador avisa.

## Material bruto dos cases

A pasta `cases/` guarda o material como chegou (PNGs de 30 MB, .mov, .psb de
300 MB) e fica **fora do repositório** pelo `.gitignore`: o GitHub recusa
arquivos acima de 100 MB. O que vai para o ar são as versões tratadas em
`assets/` — vídeos em H.264 1500k (horizontais, lado maior 1920) ou 1200k
(verticais, 720×1280), fotos recortadas no aspecto de cada cartão e uma versão
inteira `-full` para o clique em "Ampliar".
