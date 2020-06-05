def type_check(func):
    def wrapper(*args, **kargs):

        info = func.__annotations__
        for inf in info:
            if inf in kargs.keys() and not isinstance(kargs[inf], info[inf]):
                raise Exception('ERROR!!!')
        
        var = func.__code__.co_varnames
        
        i = 0
        for v in var:
            if i < len(var) and v in info.keys() and not isinstance(args[i], info[v]):
                raise Exception(f'ERROR!!! LOS PARAMETROS DE LA FUNCION {func.__name__} ESTAN MAL ESPECIFICADOS.')
            i += 1
        
        f = func(*args, **kargs)
        
        if 'return' in info.keys() and info['return'] != None and not isinstance(f, info['return']):
            raise Exception(f'ERROR!!! LA FUNCION {func.__name__} NO DEVUELVE EL TIPO ESPECIFICADO.')
        
        return f
    return wrapper

@type_check
def f1(x : int, y : str) -> str:
    return y * x

@type_check
def f2(name : str) -> None:
    print(f'hello {name}')

# print(f1(3, '8'))
# f2('ariel')