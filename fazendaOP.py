import json
import os

ARQUIVO_ANIMAIS = "animais.json"
ARQUIVO_FUNCIONARIOS = "funcionarios.json"
FUNC_PREDEFINIDOS = {
    '005': {'nome': 'Joaquim', 'cargo': 'Veterinário'},
    '008': {'nome': 'Marcelo', 'cargo': 'Gerente'},
    '015': {'nome': 'Cristina', 'cargo': 'Secretária'},
    '018': {'nome': 'Laysa', 'cargo': 'Supervisora'},
    '021': {'nome': 'Mellissa', 'cargo': 'Coordenadora'},
    '040': {'nome': 'Eduardo', 'cargo': 'Tratador'}
}
ARQUIVO_VENDAS = "vendas.json"

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(dados, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def menu_animal():
    print('''
---- MENU ANIMAL ----
1. Cadastrar Animal
2. Listar Animais
3. Buscar Animal
4. Atualizar Animal
5. Excluir Animal
0. Voltar''')

def cadastrar():
    animais = carregar_dados(ARQUIVO_ANIMAIS)

    RACAS = {'1': 'Nelore', '2': 'InduBrasil', '3': 'Holandesa', '4': 'Gir', '5': 'Girolando'}
    PELAGENS = {'1': 'Branca', '2': 'Cinza', '3': 'Amarela', '4': 'Malhada Preta', '5': 'Malhada Vermelha'}

    print("\n---- CADASTRO DE ANIMAL ----")
    nmr_id = input("Numeração do animal: ").strip()

    if any(a['id'] == nmr_id for a in animais):
        print("Erro: Animal já cadastrado!")
        return

    print("\nRaças disponíveis:")
    [print(f"{k}. {v}") for k, v in RACAS.items()]
    raca = RACAS.get(input("Número da raça: "), "Raça não especificada")

    print("\nPelagens disponíveis:")
    [print(f"{k}. {v}") for k, v in PELAGENS.items()]
    pelagem = PELAGENS.get(input("Número da pelagem: "), "Pelagem não especificada")

    nome = input("Nome do animal: ").strip()
    idade = int(input("Idade: "))

    animais.append({'id' : nmr_id, 'raça': raca ,'pelagem': pelagem , 'nome': nome , 'idade': idade})
    salvar_dados(animais, ARQUIVO_ANIMAIS)
    print("Animal cadastrado!")

def listar(animais):
    if len(animais)== 0:
        print("Estamos sem gado! Nenhum animal cadastrado.")
    else:
        print('---- NOSSO GADO CADASTRADO ----')
        for animal in animais:
            print (f"""
ID: {animal['id']},
Nome: {animal['nome']},
Raça: {animal['raça']},
Pelagem: {animal['pelagem']},
Idade: {int(animal['idade'])} anos
""")

def buscar(animais):
    nmr_animal = input("\nDigite a numeração do animal: ").strip()
    for animal in animais:
        if animal['id'] == nmr_animal:
            print(f"""
---- DADOS DO GADO ----
ID: {animal['id']}
Nome: {animal['nome']}
Raça: {animal['raça']}
Pelagem: {animal['pelagem']}
Idade: {animal['idade']} anos""")
            break
        if animal not in animais:
            print(f"\nAnimal com ID {nmr_animal} não encontrado!")

def atualizar(animais):
    nmr_animal = input("\nDigite o ID do animal: ").strip()

    animal_encontrado = None
    indice = -1
    for i, animal in enumerate(animais):
        if animal['id'] == nmr_animal:
            animal_encontrado = animal
            indice = i
            break
    
    if not animal_encontrado:
        print(f"\nAnimal com ID {nmr_animal} não encontrado!")
        return
    
    print("\nDados atuais do animal:")
    print(f"Nome: {animal_encontrado['nome']}")
    print(f"Idade: {animal_encontrado['idade']}")
    print(f"Raça: {animal_encontrado['raça']} (não editável)")
    print(f"Pelagem: {animal_encontrado['pelagem']} (não editável)")
    
    print("\nDeixe em branco para manter o valor atual")
    novo_nome = input("Novo nome: ").strip()
    nova_idade = input("Nova idade: ").strip()
    
    if not novo_nome and not nova_idade:
        print("\nNenhuma alteração foi feita.")
        return
    
    if novo_nome:
        animal_encontrado['nome'] = novo_nome
    if nova_idade:
        try:
            animal_encontrado['idade'] = int(nova_idade)
        except ValueError:
            print("\nErro: Idade deve ser um número inteiro!")
            return
    
    confirma = input('Confirmar alterações? (s/n): ').strip().lower()
    if confirma == 's':
        animais[indice] = animal_encontrado
        salvar_dados(animais, ARQUIVO_ANIMAIS)
        print("\nDados atualizados com sucesso!")
    else:
        print("\nAlterações canceladas.")

def excluir(animais):
        nmr_animal = input("\nDigite a numeração do animal: ").strip()
        for i, animal in enumerate(animais):
            if animal['id'] == nmr_animal:
                print(f"\nDados do animal a ser excluído:")
                print(f"ID: {animal['id']}")
                print(f"Nome: {animal['nome']}")
            
                confirmacao = input("\nTem certeza que deseja excluir? (s/n): ").strip().lower()
                if confirmacao == 's':
                    del animais[i]
                    salvar_dados(animais, ARQUIVO_ANIMAIS)
                    print("\nAnimal excluído com sucesso!")
                elif confirmacao == 'n':
                    print("\nOperação cancelada!")
                    break
        print(f"Animal com ID {nmr_animal} não encontrado!")


def menu_funcionario():
    print('''
---- MENU FUNCIONÁRIO ---
1. Chamar Funcionário
2. Cadastrar novo funcionário
0. Voltar
''')

def chamar_funcionario():
    try:
        historico_chamadas = carregar_dados(ARQUIVO_FUNCIONARIOS) or []
    except:
        historico_chamadas = []

    while True:
        print("\n---- CHAMADA DE FUNCIONÁRIOS ----")
        print("\nFuncionários disponíveis:")
        for cod, func in FUNC_PREDEFINIDOS.items():
            print(f"Código: {cod} | Nome: {func['nome']} | Cargo: {func['cargo']}")
        
        codigo = input("\nDigite o código do funcionário (ou 's' para sair): ").strip()
        
        if codigo.lower() == 's':
            break
        if codigo in FUNC_PREDEFINIDOS:
            funcionario = FUNC_PREDEFINIDOS[codigo]
            print(f"\nChamando: {funcionario['nome']} - {funcionario['cargo']}")

            registro = {
                'codigo': codigo,
                'nome': funcionario['nome'],
                'cargo': funcionario['cargo']
            }
            historico_chamadas.append(registro)
            salvar_dados(historico_chamadas, ARQUIVO_FUNCIONARIOS)
            print("Chamada registrada com sucesso!")
        else:
            print("Código inválido! Tente novamente ou digite 's' para sair.")

def cadastrar_funcionario():
    print("\n---- CADASTRO DE NOVOS FUNCIONÁRIOS ----")
    
    while True:
        print("\nFuncionários atuais:")
        for cod, func in FUNC_PREDEFINIDOS.items():
            print(f"Código: {cod} | Nome: {func['nome']}")
        
        codigo = input("\nDigite o código do novo funcionário (3 dígitos) ou 's' para sair: ").strip()
        
        if codigo.lower() == 's':
            break
        if codigo in FUNC_PREDEFINIDOS:
            print("Este código já está em uso!")
            continue
            
        if not codigo.isdigit() or len(codigo) != 3:
            print("Código inválido! Deve conter exatamente 3 dígitos.")
            continue
            
        nome = input("Nome completo: ").strip()
        if not nome:
            print("O nome é obrigatório!")
            continue
            
        cargo = input("Cargo: ").strip()
        if not cargo:
            print("O cargo é obrigatório!")
            continue

        FUNC_PREDEFINIDOS[codigo] = {'nome': nome, 'cargo': cargo}
        print(f"\nFuncionário {nome} cadastrado com sucesso como {cargo}!")

        continuar = input("Deseja cadastrar outro funcionário? (s/n): ").strip().lower()
        if continuar != 's':
            break


def menu_venda():
    print('''
--- MENU VENDA ----
1. Registrar Venda
0. Voltar''')

def registrar_venda():
    vendas = carregar_dados(ARQUIVO_VENDAS) or []
    animais = carregar_dados(ARQUIVO_ANIMAIS) or []
    funcionarios = carregar_dados(ARQUIVO_FUNCIONARIOS) or []
    
    print("\n---- REGISTRO DE VENDA ----")
    
    id_animal = input("ID do animal vendido: ").strip()
    animal_encontrado = next((a for a in animais if a['id'] == id_animal), None)
    
    if not animal_encontrado:
        print("Erro: Animal não cadastrado!")
        return
    
    comprador = input("Nome do comprador: ").strip()
    valor = float(input("Valor da venda (R$): "))
    print("\nFuncionários disponíveis:")
    for func in funcionarios:
        print(f"ID: {func.get('codigo', 'N/A')} | Nome: {func.get('nome', 'N/A')} | Cargo: {func.get('cargo', 'N/A')}")

    id_funcionario = input("\nID do funcionário responsável: ").strip()
    funcionario_resp = next((f for f in funcionarios if f.get('codigo') == id_funcionario), None)
    
    if not funcionario_resp:
        print("Erro: Funcionário não encontrado!")
        return
    data_venda = input("Data da venda (DD/MM/AAAA): ").strip()

    nova_venda = {
        'id_animal': id_animal,
        'animal_info': { 
            'nome': animal_encontrado.get('nome', ''),
            'raca': animal_encontrado.get('raça', ''),
            'idade': animal_encontrado.get('idade', '')
        },
        'data': data_venda,
        'comprador': comprador,
        'valor': valor,
        'responsavel': {
            'id': id_funcionario,
            'nome': funcionario_resp.get('nome', ''),
            'cargo': funcionario_resp.get('cargo', '')
        }
    }

    vendas.append(nova_venda)
    salvar_dados(vendas, ARQUIVO_VENDAS)
    print("\nVenda registrada com sucesso!")
    print(f"Animal: {animal_encontrado.get('nome', '')} vendido para {comprador} por R$ {valor:.2f}")
    print(f"Responsável: {funcionario_resp.get('nome', '')} ({funcionario_resp.get('cargo', '')})")


def main():
    while True:
        print('''
---- SISTEMA FAZENDA OURO PRETO ----
1. Gerenciar Animais
2. Gerenciar Funcionários
3. Gerenciar Vendas
0. Sair''')

        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            while True:
                menu_animal()
                animais= carregar_dados(ARQUIVO_ANIMAIS)
                sub_opção = input("\nSub Opção: ").strip()
                if sub_opção == '1':
                    cadastrar()
                if sub_opção == '2':
                    listar(animais)
                if sub_opção == '3':
                    buscar(animais)
                if sub_opção =='4':
                    atualizar(animais)
                if sub_opção == '5':
                    excluir(animais)
                if sub_opção == '0':
                    break
        elif opcao == '2':
            while True:
                menu_funcionario()
                funciorarios = carregar_dados(ARQUIVO_FUNCIONARIOS)
                sub_opção = input("\nSub Opção: ").strip()
                if sub_opção == '1':
                    chamar_funcionario()
                if sub_opção == '2':
                    cadastrar_funcionario()
                if sub_opção == '0':
                    break
        if opcao == '3':
            while True:
                menu_venda()
                vendas = carregar_dados(ARQUIVO_VENDAS)
                sub_opção = input("\nSub Opção: ").strip()
                if sub_opção == '1':
                    registrar_venda()
                if sub_opção == '0':
                    break
        elif opcao == '0':
            print("\nSaindo do sistema...")
        else:
            print("\nOpção inválida!")

main ()
