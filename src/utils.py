import json
import socket
import inspect


def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
    return ip


def get_name():
    name = socket.gethostname()
    return name


def dictToStr(dict):
    for key in dict.keys():
        dict[key] = str(dict[key])
    return dict


def dict_to_binary(the_dict):
    x = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in x)
    return binary


def nozero(valor):
    if valor == 0:
        return 1
    return valor


def verdadeiro(texto):
    return texto == '1'


def distintos(lista):
    return [i for n, i in enumerate(lista) if i not in list[n + 1:]]


def isEmptyOrNull(valor):
    return valor == "" or valor is None


def imprimeDados(data):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    arg = [var_name for var_name, var_val in callers_local_vars if var_val is data]
    arg = type(data) if len(arg) == 0 else arg[0]

    print('\n' * 3)
    print('%' * 80)

    print(f'{arg} ==>', data)

    if type(data) == dict:
        print('-'*80)
        imprimeJson(data)
    elif type(data) == list:
        print('-'*80)
        for e in data:
            print(e)
    elif type(data) == str:
        pass
    elif type(data) == int:
        pass
    else:
        print(f'O imprime Dados não pode reconhecer o tipo {type(data)}')

    print('%' * 80)
    print('\n' * 3)


def imprimeJson(data):
    if type(data) == str:
        try:
            data = json.loads(data)
            print(json.dumps(data, indent=4, sort_keys=True))
        except Exception as e:
            print(data)

    elif type(data) == dict:
        print(json.dumps(data, indent=4, sort_keys=True))


def str2sql(data, vazio=False):
    xnull = 'NULL'
    if vazio:
        xnull = f"''"
    if not data:
        return xnull
    if type(data) is int:
        return data
    if type(data) is float:
        return data
    if data is None:
        return xnull
    if len(data) == 0:
        return xnull
    return f"'{data}'"
