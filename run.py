from src.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
Esse arquivo é a chave de ignição da aplicação.

>> from src.app import create_app
    Aqui ele importa o metodo create_app contido no __init__ da pasta app.
    Sem isso o run.py não saberia como construir seu projeto. É como um manual de instruções.

>> app = create_app()
    Aqui ele coloca no app a aplicação flask contida no __init__ da pasta app.

>> if __name__ == '__main__':
    Aqui ele permite que seu projeto tenho uma "vida dupla". 
    Para fazer essa distinção, o Python cria uma variável chamada __nome__ para cada script.
    O valor dessa variável muda dependendo de como o script está sendo usado. 
    
    - Cenário 1 - Executando o Arquivo Diretamente:
    Quando você vai ao seu terminal e executa seu arquivo diretamente:
        >> python run.py
        ou
        >> flask run
    Você está dizendo ao Python: "run.py é o programa principal, a estrela do show de hoje".
    Neste caso, o Python automaticamente define a variável __name__ com o valor especial  "__main__".
    Portanto, a verificação...    
        >> if __name__ == '__main__':  # A condição se torna: if "__main__" == "__main__": true
    
    - Cenário 2 - Importando o Arquivo: 
    Agora, imagine um ambiente de produção. O servidor Gunicorn precisa da sua aplicação, mas ele mesmo quer ser o "programa principal".
    Então, o Gunicorn importa o seu arquivo run.py, mais ou menos assim:
        # O que o Gunicorn faz nos bastidores
        >> import run
        # Agora o Gunicorn usa a variável 'app' que foi criada em run.py
        >> gunicorn_server.run(run.app)
    
    Quando o arquivo run.py é importado por outro script, o Python define a variável __name__ com o nome do próprio arquivo, sem a extensão .py.
    Neste caso, o Python define __name__ = "run".
    Portanto, a verificação...
        >> if __name__ == '__main__':  # A condição se torna: if "run" == "__main__": false
        
    Em resumo: O if __name__ == '__main__': é o jeito padrão do Python de dizer:
    "Execute este pedaço de código apenas quando este arquivo for o programa principal,
    e não quando ele for apenas um coadjuvante importado por outro programa".

>> app.run(debug=True)
    Aqui é iniciado o servidor de desenvolvimento embutido do flask.
    O "debug=True" ativa 2 coisas:
        1. Recarregamento automático: o servidor reinicia sozinho toda vez que você salva alguma alteração no código.
        2. Depurador interativo: se ocorrer algum erro o flask mostra uma página de erro detalhada no navegador, em vez de uma mensagem genérica.
"""