from flask import Flask # importa a classe principal da biblioteca flask
from config import Config # vai até o arquivo config.py e importa a classe Config - É como pegar o manual de especificações
from . import db # o . significa que é o mesmo pacote. Da as funções get_db, close_db e init_app - É como chamar a equipe de instalação do motor

from .routes import home_routes

def create_app():
    """
    Essa é a Application Factory. Ela cria, configura e monta a aplicação Flask.
    """
    app = Flask(__name__)
    # Cria a instância principal da aplicação, um objeto Flask.
    # O parâmetro __name__ é uma variável especial que contém o nome do módulo atual

    app.config.from_object(Config) # Diz a aplicação app (objeto de Flask) para aplicar as configurações de Config.

    db.init_app(app) # garante que a limpeza do banco de dados aconteça automaticamente

    app.register_blueprint(home_routes.bp)

    return app

"""
    Pense em cada arquivo .py que você cria como uma pessoa com uma etiqueta de identificação (um crachá).
    O valor da variável __name__ é o que está escrito nesse crachá.
    - O Python tem uma regra simples: o que está escrito no crachá depende do papel que a pessoa (o arquivo) está desempenhando naquele momento.
    
    Um arquivo Python pode desempenhar dois papéis:
        1. O Protagonista: Quando você executa o arquivo diretamente no terminal. Ele é o programa principal, a estrela do show.
        2. O Coadjuvante: Quando o arquivo é importado por outro arquivo. Ele está lá para fornecer ferramentas e funções para o protagonista.

    A variável __name__ muda de valor para refletir qual desses dois papéis o arquivo está desempenhando.
"""
"""
    ### Cenário 1: O Arquivo é o Protagonista
    Vamos criar um arquivo simples chamado meu_script.py.
        # meu_script.py
        >> print(f"O crachá deste arquivo diz: {__name__}")
    
    Agora, vamos ao terminal e executamos este arquivo diretamente:
        >> python meu_script.py
    A saída será:
        >> O crachá deste arquivo diz: __main__
    
    Análise:
    Quando um arquivo é o programa principal (executado diretamente), o Python escreve a palavra especial __main__ no seu crachá. 
    Isso significa "o ponto de partida", "o principal".
    
"""
"""
    ### Cenário 2: O Arquivo é o Coadjuvante
    Agora, vamos criar um segundo arquivo, chamado programa_principal.py, que vai importar o nosso primeiro script.
        # programa_principal.py
        >> print("Vou chamar meu amigo, o coadjuvante...")
        # Ao importar 'meu_script', o código dentro dele é executado na hora.
        import meu_script
        print("Pronto, já chamei.")
        print(f"O crachá do programa_principal.py diz: {__name__}")
    
    Agora, vamos executar o programa_principal.py:
        >> python programa_principal.py
    
    A saída será:
        # Vou chamar meu amigo, o coadjuvante...
        # O crachá deste arquivo diz: meu_script
        # Pronto, já chamei.
        # O crachá do programa_principal.py diz: __main__
    
    Análise:
    - Começamos a executar programa_principal.py, então o crachá dele é __main__.
    - Quando ele importa meu_script, o Python executa o código de meu_script.
    - Desta vez, como meu_script não é o protagonista (ele é um coadjuvante importado), 
      o Python escreve o nome do próprio arquivo (meu_script) no seu crachá __name__.
    - A execução volta para programa_principal.py, que confirma que o seu próprio crachá ainda diz __main__.
"""
"""
    ### Conectando com o Flask: app = Flask(__name__)
    Agora, vamos aplicar isso ao seu código: app = Flask(__name__).
    Quando você cria a sua aplicação dentro do arquivo src/app/__init__.py, o __name__ que você passa para o Flask não é __main__.

    Seu programa principal é run.py.    
    run.py importa a função create_app de src.app.
    
    Quando o código em src/app/__init__.py é executado, ele é um coadjuvante.
    Portanto, o valor de __name__ dentro daquele arquivo será o nome do pacote: 'src.app'.
    
    Você está, na prática, executando: app = Flask('src.app').
"""