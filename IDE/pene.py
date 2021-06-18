import pathlib
init_route=pathlib.Path(__file__).parent.parent
init_route=init_route /'SoftWare'/ 'LexicalAnalizer'/'compile.py'
print(init_route.absolute())