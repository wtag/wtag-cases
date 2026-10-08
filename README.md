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

Capa → divisor CASES → por cliente, capa + cases → fecho.

| Cliente | Cases |
|---|---|
| Sicredi Serrana | 40 Anos · Clubinho da Poupança · Private · Horóscopo do Golpe |
| Magalu | Craques Gigantes · Lojinha do Fiuk |
| Keeta | Central do Corre · Pulando o Bloco · Brasil Corre |
| Bridgestone | Seu Pneu de Carro Novo |
| Multiplan | BarraShoppingSul · Golden Lake |

## Ocultar e mostrar cases

**1 · No arquivo — muda o link para todo mundo.** No topo do `index.html` está a
lista `window.CASES`. Troque `true` por `false` para tirar um case; `false` por
`true` para trazer de volta. O slide continua no arquivo, só sai da
apresentação, do sumário e do rodapé. A **capa do cliente some sozinha** quando
todos os cases dele estão ocultos.

**2 · No endereço — um recorte por envio, sem republicar.**

| Endereço | Mostra |
|---|---|
| `…/?so=keeta,magalu` | só esses clientes |
| `…/?so=sicredi&sem=private` | Sicredi, menos o Private |
| `…/?sem=bridgestone,horoscopo` | tudo, menos esses |

Vale o nome do cliente (`sicredi`, `magalu`, `keeta`, `bridgestone`,
`multiplan`) ou o id do case sem o `s-` (`private`, `horoscopo`,
`lojinha-fiuk`…). O endereço **só estreita**: um case marcado `false` no arquivo
não volta por link.

## Cache

`css/deck.css`, `js/*.js` entram com `?v=NN` no `index.html`. Editou um deles,
suba o número em todas as linhas:

```bash
sed -i '' 's/?v=1"/?v=2"/g' index.html
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
