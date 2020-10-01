from cmp.pycompiler import Symbol, Epsilon, Sentence, Production, Grammar, Item
from cmp.parsers import Action
from cmp.automata import State

class HtmlFormatter:

    EOL = '\n'
    ArrowToHtml = '<span class="grammarArrow"> -> </span>'
    OrToHtml = '<span class="grammarOr"> | </span>'
    DotToHtml = '<span class="grammarDot"> . </span>'

    def SymbolToHtml(s):
        return f'<span class="grammarSymbol">{s}</span>'

    def EpsilonToHtml(e):
        return f'<span class="grammarEpsilon">{e}</span>'

    def SentenceToHtml(s):
        return HtmlFormatter.CollectionToHtml(s, ' ')

    def ProductionToHtml(p):
        return '%s%s%s' % (HtmlFormatter.SymbolToHtml(p.Left), HtmlFormatter.ArrowToHtml,
                            HtmlFormatter.CustomToHtml(p.Right))

    def NtProductionsToHtml(nt):
        return '%s%s%s' % (HtmlFormatter.SymbolToHtml(nt), HtmlFormatter.ArrowToHtml,
                            HtmlFormatter.CollectionToHtml([p.Right for p in nt.productions], HtmlFormatter.OrToHtml))

    def ActionToHtml(a):
        action, tag = a
        return '%s%s' % ('<span style="color: gray">S</span>' if action == Action.SHIFT else '<span style="color: green">OK</span>' if action == Action.OK else '',
                        HtmlFormatter.CustomToHtml(tag))

    def ItemToHtml(i):
        return '%s%s%s%s%s, { %s }' % (HtmlFormatter.SymbolToHtml(i.production.Left), HtmlFormatter.ArrowToHtml,
                                        HtmlFormatter.CollectionToHtml(i.production.Right[:i.pos], ' '), 
                                        HtmlFormatter.DotToHtml,
                                        HtmlFormatter.CollectionToHtml(i.production.Right[i.pos:], ' '), 
                                        HtmlFormatter.CollectionToHtml(i.lookaheads))

    def CustomToHtml(c):
        if isinstance(c, Symbol):
            return HtmlFormatter.SymbolToHtml(c)
        if isinstance(c, Epsilon):
            return HtmlFormatter.EpsilonToHtml(c)
        if isinstance(c, Sentence):
            return HtmlFormatter.SentenceToHtml(c)
        if isinstance(c, Production):
            return HtmlFormatter.ProductionToHtml(c)
        if isinstance(c, Item):
            return HtmlFormatter.ItemToHtml(c)
        if isinstance(c, State):
            return HtmlFormatter.CustomToHtml(c.state)
        if isinstance(c, Action):
            return HtmlFormatter.ActionToHtml(c)
        return f'<span style="color: red"><strong>{c}</strong></span>'

    def FormatCollection(c):
        return [HtmlFormatter.CustomToHtml(item) for item in c]

    def CollectionToHtml(c, sep=', ', formatter=None):
        return sep.join([formatter(item) for item in c] if formatter else HtmlFormatter.FormatCollection(c))

    def GrammarToHtml(G):
        return f'''<dl>
                <dt><strong>Terminales:</strong></dt> 
                <dd><p>{HtmlFormatter.CollectionToHtml(G.terminals)}</p></dd>
                <dt><strong>No Terminales:</strong></dt> 
                <dd><p>{HtmlFormatter.CollectionToHtml(G.nonTerminals)}</p></dd>
                <dt><strong>Producciones:</strong></dt>
                <dd><p>{HtmlFormatter.CollectionToHtml(G.nonTerminals, '</p><p>', HtmlFormatter.NtProductionsToHtml)}</p></dd>
                </dl>'''

    def FirstsToHtml(G, firsts):
        sf = lambda s: '<p>FIRST(%s) = { %s }</p>' % (HtmlFormatter.SymbolToHtml(s), HtmlFormatter.CollectionToHtml(firsts[s].items()))
        pf = lambda p: '<p>FIRST(%s) = { %s }</p>' % (HtmlFormatter.ProductionToHtml(p), HtmlFormatter.CollectionToHtml(firsts[p.Right].items()))

        return f'''<dl>
                <dt><strong>No Terminales:</strong></dt> 
                <dd>{HtmlFormatter.CollectionToHtml(G.nonTerminals, HtmlFormatter.EOL, sf)}</dd>
                <dt><strong>Producciones:</strong></dt>
                <dd>{HtmlFormatter.CollectionToHtml(G.Productions, HtmlFormatter.EOL, pf)}</dd>
                </dl>'''

    def FollowsToHtml(G, follows):
        sf = lambda s: '<p>FOLLOW(%s) = { %s }</p>' % (HtmlFormatter.SymbolToHtml(s), HtmlFormatter.CollectionToHtml(follows[s]))

        return f'''<dl>
                <dt><strong>No Terminales:</strong></dt>
                <dd>{HtmlFormatter.CollectionToHtml(G.nonTerminals, HtmlFormatter.EOL, sf)}</dd>
                </dl>'''

    def CellClass(row, symbol): 
        return f'''<td {'class="errorCell"' if symbol in row and len(row[symbol]) > 1 else ''} title="{symbol}">'''

    def LL1TableToHtml(G, table, label=''):
        return f'''<table>
                    <tr><th>{label}</th><th>{HtmlFormatter.CollectionToHtml(G.terminals, '</th><th>')}</th>
                    {''.join(f'<tr><th>{HtmlFormatter.SymbolToHtml(nt)}</th>'
                            + ''.join(f'{HtmlFormatter.CellClass(row, t)}<p>' + 
                            (HtmlFormatter.CollectionToHtml(row[t], '</p><p>') if t in row else '-----') + '</p></td>'
                                for t in G.terminals) + '</tr>'
                        for nt, row in table.items())}
                    </table>'''

    def ItemsCollectionToHtml(automaton):
        ni = lambda i: f'<p class="itemCollection">{HtmlFormatter.CustomToHtml(i)}</p>'
        nr = lambda n: f'''<table>
                        <tr><th>I<sub>{n.idx}</sub>:</th></tr>
                        <tr><td>{HtmlFormatter.CollectionToHtml(n.state, HtmlFormatter.EOL, ni)}</td></tr>
                        </table>'''

        return HtmlFormatter.CollectionToHtml(automaton, HtmlFormatter.EOL, nr)

    def ActionGotoTableToHtml(table, columns, label=''):
        cs = lambda c: f'<th>{HtmlFormatter.SymbolToHtml(c)}</th>'
        cl = lambda c: f'<p>{HtmlFormatter.CustomToHtml(c)}</p>'    
        return f'''<table>
                    <tr><th>{label}</th>{HtmlFormatter.CollectionToHtml(columns, HtmlFormatter.EOL, cs)}</tr>
                    {''.join('<tr>' + f'<th>I<sub>{idx}</sub></th>' + ''.join(HtmlFormatter.CellClass(row, symbol) +
                            (HtmlFormatter.CollectionToHtml(row[symbol], '', cl) if symbol in row else '-----')  + '</td>'
                                for symbol in columns) + '</tr>' 
                        for idx, row in table.items())}
                    </table>'''

    def DerivationsToHtml(words, derivations):
        dr = lambda d: HtmlFormatter.ErrorMessageToHtml('Error al parsear') if d is None else d 
        wd = lambda c: f'<table><tr><th>{HtmlFormatter.CollectionToHtml(c[0])}</th></tr><tr><td>{dr(c[1])}</td></tr></table>'

        return HtmlFormatter.CollectionToHtml(zip(words, derivations), HtmlFormatter.EOL, wd)

    def ErrorMessageToHtml(msg):
        return f'<h3 class="error">• {msg}</h3>'

    def MessageToHtml(msg):
        return f'<h3>• {msg}</h3>'

    def GoodMessageToHtml(msg):
        return f'<h3 class="good">• {msg}</h3>'
