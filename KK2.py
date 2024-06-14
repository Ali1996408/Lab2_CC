class CFG:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def remove_left_recursion(self):
        new_productions = {}
        new_non_terminals = set(self.non_terminals)  # Копия для добавления новых нетерминалов

        for non_terminal in self.non_terminals:
            new_productions[non_terminal] = []
            immediate_recursions = []
            others = []

            for production in self.productions.get(non_terminal, []):
                if production.startswith(non_terminal):
                    immediate_recursions.append(production[1:])
                else:
                    others.append(production)

            if immediate_recursions:
                new_non_terminal = non_terminal + "'"
                while new_non_terminal in self.non_terminals or new_non_terminal in new_productions:
                    new_non_terminal += "'"
                new_non_terminals.add(new_non_terminal)
                new_productions[new_non_terminal] = []
                for production in others:
                    new_productions[non_terminal].append(production + new_non_terminal)

                for recursion in immediate_recursions:
                    new_productions[new_non_terminal].append(recursion + new_non_terminal)
                # Добавление ε продукции для нового не терминала
                new_productions[new_non_terminal].append('ε')
            else:
                new_productions[non_terminal].extend(others)

        self.non_terminals = new_non_terminals
        self.productions = new_productions

    def __str__(self):
        result = []
        for non_terminal in self.productions:
            productions = [prod if prod != '' else 'ε' for prod in self.productions[non_terminal]]
            result.append(f"{non_terminal} -> {' | '.join(productions)}")
        return '\n'.join(result)


def reachable_symbols(cfg):
    reachable = set()
    reachable.add(cfg.start_symbol)
    to_check = [cfg.start_symbol]

    while to_check:
        current = to_check.pop()
        for production in cfg.productions.get(current, []):
            for symbol in production:
                if symbol in cfg.non_terminals and symbol not in reachable:
                    reachable.add(symbol)
                    to_check.append(symbol)
    return reachable


def remove_unreachable_symbols(cfg):
    reachable = reachable_symbols(cfg)
    new_productions = {k: v for k, v in cfg.productions.items() if k in reachable}
    new_non_terminals = {nt for nt in cfg.non_terminals if nt in reachable}
    new_cfg = CFG(new_non_terminals, cfg.terminals, new_productions, cfg.start_symbol)

    return new_cfg


# Пример использования:
non_terminals = {'S', 'A', 'B'}
terminals = {'a', 'b'}
productions = {
    'S': ['Sa', 'Sb', 'a', 'b'],
    'A': ['Sb', 'a'],
    'B': ['b']
}
start_symbol = 'S'

cfg = CFG(non_terminals, terminals, productions, start_symbol)
print("Исходная грамматика:")
print(cfg)

cfg.remove_left_recursion()
print("\nГрамматика после устранения левой рекурсии:")
print(cfg)

cfg = remove_unreachable_symbols(cfg)
print("\nГрамматика после удаления недостижимых символов:")
print(cfg)
