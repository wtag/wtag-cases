/* ============================================================================
   WT.AG · CASES — quais telas entram
   ============================================================================
   A LISTA não mora aqui: fica no topo do index.html, em window.CASES, para ser
   a primeira coisa que se vê ao abrir o arquivo. Este script só a aplica, e
   precisa rodar ANTES do deck.js, que lê os slides visíveis uma vez só, ao
   carregar — por isso a ordem dos <script> no fim do index.html.

   Ocultar é pôr data-oculto na <section>, o mesmo atributo que o deck já
   respeita: o slide continua no HTML e só sai da navegação, do sumário e dos
   pontinhos do rodapé.

   Três camadas, nesta ordem:
     1. window.CASES (index.html) — o padrão do link. false = nunca aparece.
     2. ?so=  no endereço — mostra SÓ estes, dentre os que estão true.
     3. ?sem= no endereço — tira estes, dentre os que sobraram.
   A URL só estreita, nunca reabre: um case marcado false no arquivo não volta
   por link. Assim dá para mandar um recorte por prospect sem republicar, e sem
   o risco de um link expor um case que foi tirado de propósito.

   Nos parâmetros vale o nome do cliente (odontoprev, multiplan, keeta, sicredi,
   magalu, bridgestone) ou o id do case, com ou sem o "s-" na frente:
     ?so=keeta,magalu
     ?so=sicredi&sem=private,horoscopo
     ?sem=bridgestone

   A capa de cada cliente não tem chave própria: aparece enquanto houver ao
   menos um case dele visível e some sozinha quando todos saem. A chave geral
   window.CAPAS = false (index.html) tira todas de uma vez.
   ========================================================================= */
(function () {
  'use strict';

  var CASES = window.CASES || {};

  function lista(nome) {
    var m = new RegExp('[?&]' + nome + '=([^&#]*)').exec(location.search);
    if (!m) return null;
    return decodeURIComponent(m[1]).toLowerCase().split(',')
      .map(function (s) { return s.trim().replace(/^s-/, ''); })
      .filter(Boolean);
  }
  var so  = lista('so');
  var sem = lista('sem') || [];

  function casa(sec, termos) {
    var id = sec.id.replace(/^s-/, '');
    return termos.indexOf(id) >= 0 || termos.indexOf(sec.dataset.ato) >= 0;
  }

  var visiveisPorCliente = {};
  [].forEach.call(document.querySelectorAll('.slide.case'), function (sec) {
    var mostrar = CASES[sec.id] !== false;
    if (!(sec.id in CASES)) {
      /* Case novo que entrou no HTML e não na lista: aparece, mas avisa — senão
         ele fica fora do controle sem ninguém perceber. */
      console.warn('[cases] "' + sec.id + '" não está em window.CASES; entra como visível.');
    }
    if (mostrar && so)                    mostrar = casa(sec, so);
    if (mostrar && sem.length)            mostrar = !casa(sec, sem);
    if (mostrar) {
      sec.removeAttribute('data-oculto');
      visiveisPorCliente[sec.dataset.ato] = true;
    } else {
      sec.setAttribute('data-oculto', '');
    }
  });

  [].forEach.call(document.querySelectorAll('.slide[data-capa]'), function (capa) {
    if (window.CAPAS !== false && visiveisPorCliente[capa.dataset.ato]) capa.removeAttribute('data-oculto');
    else capa.setAttribute('data-oculto', '');
  });

  /* "1…N" nas instruções da capa: N é o total que de fato está no ar. */
  var total = document.querySelectorAll('.slide:not([data-oculto])').length;
  [].forEach.call(document.querySelectorAll('.nav__total'), function (k) {
    k.textContent = total;
  });
})();
