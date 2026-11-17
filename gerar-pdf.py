#!/usr/bin/env python3
"""
PDF de uma opção da apresentação de cases.

    python3 gerar-pdf.py 01            # opção 01 de window.OPCOES
    python3 gerar-pdf.py               # sem opção: o que window.CASES deixa no ar
    python3 gerar-pdf.py 01 --saida "/caminho/da/pasta"

O index.html é a única fonte: o script lê a lista da opção (ou window.CASES),
monta as páginas na ordem dela e imprime pelo Chrome headless, parado no quadro
final de cada tela. Mesma técnica do gerar-pdf.py do Credenciais v2:
  · cada <section> vira uma página 1920×1080 (css/pdf.css);
  · data-lazy vira src (alta, não a -m);
  · contadores já escritos no valor final;
  · vídeo vira link para a tela do deck no ar (?opcao=NN#slide-NN);
  · a capa de instruções de navegação fica de fora (num PDF ela não diz nada).
"""

import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DECK_ONLINE = 'https://wtag.github.io/wtag-cases/'
CORES = {'escuro': '#000000', 'claro': '#F7F9EA', 'laranja': '#FF4900'}


def ler_opcao(html, num):
    """(nome, capas, [ids]) da opção, lidos do bloco window.OPCOES."""
    bloco = re.search(r"window\.OPCOES\s*=\s*\{([\s\S]*?)\n\};", html).group(1)
    m = re.search(r"'%s'\s*:\s*\{([\s\S]*?)\}" % re.escape(num), bloco)
    if not m:
        sys.exit('! a opção %s não existe em window.OPCOES' % num)
    corpo = m.group(1)
    nome = (re.search(r"nome:\s*'([^']*)'", corpo) or [0, num])[1]
    capas = 'capas: true' in corpo.replace('  ', ' ')
    ids = re.findall(r"'(s-[^']+)'", re.search(r"casos:\s*\[([\s\S]*?)\]", corpo).group(1))
    return nome, capas, ids


def ids_padrao(html):
    bloco = re.search(r"window\.CASES\s*=\s*\{([\s\S]*?)\};", html).group(1)
    ligados = re.findall(r"'(s-[^']+)'\s*:\s*true", bloco)
    capas = re.search(r"window\.CAPAS\s*=\s*false", html) is None
    return 'padrão', capas, ligados


def formatar(v, dec, sep):
    s = ('%.*f' % (dec, v)) if dec > 0 else str(int(round(v)))
    if dec > 0:
        s = s.replace('.', ',')
    if sep:
        p = s.split(',')
        p[0] = re.sub(r'\B(?=(\d{3})+(?!\d))', '.', p[0])
        s = ','.join(p)
    return s


def congelar(sec, n, opcao):
    abrir = re.match(r'<section\b[^>]*>', sec).group(0)
    tom = (re.search(r'data-tom="([^"]+)"', abrir) or [0, 'escuro'])[1]
    cor = (re.search(r'data-fundo="([^"]+)"', abrir) or [0, CORES.get(tom, '#000')])[1]
    novo = re.sub(r'class="([^"]*)"', r'class="\1 pdf-pg is-active is-played"', abrir, count=1)
    novo = novo.replace(' data-oculto', '')
    if 'style="' in novo:
        novo = re.sub(r'style="([^"]*)"', r'style="\1;background:%s"' % cor, novo, count=1)
    else:
        novo = novo[:-1] + ' style="background:%s">' % cor
    b = novo + sec[len(abrir):]
    # imagens: o src que o deck.js poria ao entrar na tela
    b = re.sub(r'(<img\b(?:(?!\ssrc=)[^>])*?)data-lazy="([^"]+)"', r'\1src="\2" data-lazy="\2"', b)
    # contadores no valor final

    def conta(m):
        at = dict(re.findall(r'data-count-(\w+)="([^"]*)"', m.group(1)))
        try:
            v = float(at['to'])
        except (KeyError, ValueError):
            return m.group(0)
        txt = at.get('pre', '') + formatar(v, int(at.get('dec') or 0), at.get('sep') == '1') + at.get('pos', '')
        return m.group(1) + txt + '</%s>' % m.group(2)
    b = re.sub(r'(<([a-z]+)\b[^>]*data-count-to="[^"]*"[^>]*>)([^<]*)</\2>', conta, b)
    # vídeos: link para a mesma tela no deck no ar
    alvo = '%s?opcao=%s#slide-%02d' % (DECK_ONLINE, opcao, n) if opcao else '%s#slide-%02d' % (DECK_ONLINE, n)
    lk = '<a class="pdf-lk" href="%s" target="_blank" rel="noopener" aria-label="Assistir ao vídeo"></a>' % alvo
    b = re.sub(r'(<\w+\b[^>]*data-video="[^"]+"[^>]*>)', lambda m: m.group(1) + lk, b)
    b = re.sub(r'(<\w+\b[^>]*data-youtube="([^"]+)"[^>]*>)',
               lambda m: m.group(1) + lk.replace(alvo, 'https://www.youtube.com/watch?v=' + m.group(2)), b)
    # esteira de repercussão: uma passada só (parada, a duplicata apareceria)
    def fita(m):
        itens = re.findall(r'<(?:span|a) class="reperc__it[\s\S]*?</(?:span|a)>', m.group(2))
        return m.group(1) + ''.join(itens[:len(itens) // 2] or itens) + '</div>'
    b = re.sub(r'(<div class="reperc__fita"[^>]*>)([\s\S]*?)</div>', fita, b)
    return b


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    num = args[0] if args else None
    saida = sys.argv[sys.argv.index('--saida') + 1] if '--saida' in sys.argv else AQUI
    html = open(os.path.join(AQUI, 'index.html'), encoding='utf-8').read()
    nome, capas, ids = ler_opcao(html, num) if num else ids_padrao(html)

    secoes = {}
    for sec in re.findall(r'<section\b[^>]*>[\s\S]*?</section>', html):
        a = re.match(r'<section\b[^>]*>', sec).group(0)
        sid = (re.search(r'id="([^"]+)"', a) or [0, None])[1]
        ato = (re.search(r'data-ato="([^"]+)"', a) or [0, ''])[1]
        secoes.setdefault('ordem', []).append((sid, ato, a, sec))
    porid = {sid: sec for sid, _, _, sec in secoes['ordem'] if sid}
    capa_de = {ato: sec for sid, ato, a, sec in secoes['ordem'] if 'data-capa' in a}
    divisor = [sec for sid, ato, a, sec in secoes['ordem'] if 'Divisor' in a]
    fecho = [sec for sid, ato, a, sec in secoes['ordem'] if ato == 'fecho']

    ordem, feitas = list(divisor), set()
    for i in ids:
        if i not in porid:
            print('  ! %s não existe no index.html' % i)
            continue
        ato = re.search(r'data-ato="([^"]+)"', porid[i]).group(1)
        if capas and ato in capa_de and ato not in feitas:
            ordem.append(capa_de[ato])
            feitas.add(ato)
        ordem.append(porid[i])
    ordem += fecho

    # n = número da tela no deck (a capa de instruções é a 1, fora do PDF)
    paginas = [congelar(sec, n + 2, num) for n, sec in enumerate(ordem)]
    doc = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
           '<title>WT.AG · Cases · %s</title>'
           '<link rel="stylesheet" href="css/deck.css"><link rel="stylesheet" href="css/pdf.css">'
           '</head><body>%s</body></html>' % (nome, '\n'.join(paginas)))
    tmp = os.path.join(AQUI, '_teste-pdf.html')
    open(tmp, 'w', encoding='utf-8').write(doc)
    pdf = os.path.join(saida, 'WT.AG_Cases_%s.pdf' % ('Opcao-' + num if num else 'Padrao'))
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--run-all-compositor-stages-before-draw',
                    '--virtual-time-budget=60000', '--no-pdf-header-footer',
                    '--print-to-pdf=' + pdf, 'file://' + tmp], capture_output=True)
    os.remove(tmp)
    if not os.path.exists(pdf):
        sys.exit('! o Chrome não gerou o PDF')
    print('%s: %d páginas · %.1f MB' % (pdf, len(paginas), os.path.getsize(pdf) / 1e6))


if __name__ == '__main__':
    main()
