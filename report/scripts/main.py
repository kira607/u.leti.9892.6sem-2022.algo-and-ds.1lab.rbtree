import helpers
import latex


def get_methods_list(file_path, full=False):
    p, brace = (0, '(') if not full else (1, ')')
    with open(file_path, 'r') as f:
        lines = f.readlines()

    methods = []

    for line in lines:
        if 'def ' in line:
            meth = line[line.find('def ') + 4:line.find(brace) + p]
            methods.append(meth.replace('_', '\\_'))
    
    return methods


def get_methods_description(methods: list):
    desc = {}
    for m in methods:
        desc[f'\\item \\verb|{m}|'] = '--- description'
    return '\n'.join(f'{k} {v}' for k, v in desc.items())


def get_complexity_table(methods):
    table = latex.LatexTable(2, caption='Оценка временной сложности методов класса RBTree', label='complexity')
    table.set_header('Метод', 'Оценка временной сложности')
    for method in methods:
        table.add_row(f'\\verb|{method}|', '$ O(n) $')
    return table.render()


def get_tests_descriptions(tests):
    desc = ''
    for test in tests:
        desc += f'\\subsection*{{{test}}}\n\n Проверяет ...\n\n'
    return desc


def get_example_subsection(ru_name, en_name):
    sec = (
        f'\\subsection{{{ru_name}}}\n'
        '\n'
        'Код примера:\n'
        '\n'
        '\\begin{lstlisting}\n'
        '\n'
        '\\end{lstlisting}\n'
        '\n'
        f'Результат выполнения примера (рис. \\ref{{fig:{en_name}}}):\n'
        '\n'
    )
    sec += latex.PictureCreator.get_picture(
        f'example_{en_name}', f'Результат выполнения операции "{ru_name.lower()}"', en_name, width='0.85\\linewidth'
    )
    sec += '\n'
    return sec


def get_examples_page(ru_names, en_names):
    page = ''
    for ru_name, en_name in zip(ru_names, en_names):
        page += get_example_subsection(ru_name, en_name)
    return page

def main():
    methods = get_methods_list('/home/kirill/programming/1lab-algo-3-2/rbtree/_rbtree.py')
    tests = get_methods_list('/home/kirill/programming/1lab-algo-3-2/rbtree/tests/test_rbtree.py', True)
    get_methods_description(methods)
    get_complexity_table(['insert', 'remove', 'find', 'clear', 'get_keys', 'get_values', 'print'])
    get_tests_descriptions(tests)
    print(get_examples_page(
        ['Поиск', 'Вставка', 'Удаление', 'Получение ключей/значений'],
        ['find', 'insert', 'remove', 'kv'],
    ))



if __name__ == '__main__':
    main()
