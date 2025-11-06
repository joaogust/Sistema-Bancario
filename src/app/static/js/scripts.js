/**
 * =================================================================
 * ARQUIVO DE SCRIPTS GLOBAIS - IFSP BANK
 * =================================================================
 *
 * Este arquivo contém todas as interações de JavaScript
 * para o front-end da aplicação.
 *
 * Funções:
 * 1. Ativação da Validação do Bootstrap
 * 2. Confirmação de Senha em tempo real
 * 3. Máscaras de Input (CPF, CEP, Dinheiro, etc.)
 * 4. Preenchimento automático de Endereço (ViaCEP)
 * 5. Envio de formulário AJAX (Ex: Modal PIX)
 *
 * =================================================================
 */

// Espera o DOM (a página) carregar completamente antes de executar o JS
document.addEventListener('DOMContentLoaded', () => {
    
    // Inicia todas as funções auxiliares
    initBootstrapValidation();
    initPasswordConfirmation();
    initInputMasks();
    initCepAutofill();
    initAjaxPixModal();

    console.log('IFSP Bank scripts carregados com sucesso.');
});


/**
 * -----------------------------------------------------------------
 * 1. Ativação da Validação do Bootstrap
 * -----------------------------------------------------------------
 * Procura todos os formulários com a classe 'needs-validation'
 * e aplica os estilos de feedback (verde/vermelho) do Bootstrap.
 */
function initBootstrapValidation() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}


/**
 * -----------------------------------------------------------------
 * 2. Confirmação de Senha
 * -----------------------------------------------------------------
 * Verifica se os campos de senha e confirmação são iguais.
 * Usado em: criar-senha.html, redefinir-senha.html
 */
function initPasswordConfirmation() {
    
    // Função genérica para checar os pares de senha
    const checkPasswords = (formSelector, passName, confirmName) => {
        const form = document.querySelector(formSelector);
        if (!form) return; // Se o formulário não está na página, sai

        const passField = form.querySelector(`input[name="${passName}"]`);
        const confirmField = form.querySelector(`input[name="${confirmName}"]`);

        if (!passField || !confirmField) return; 

        const validate = () => {
            if (passField.value !== confirmField.value) {
                // 'setCustomValidity' informa ao Bootstrap que o campo é inválido
                confirmField.setCustomValidity('As senhas não conferem.');
            } else {
                confirmField.setCustomValidity(''); // Válido
            }
        };

        passField.addEventListener('input', validate);
        confirmField.addEventListener('input', validate);
    };

    // Mapeia os formulários e campos
    // (Usando o 'action' como seletor único)
    checkPasswords('form[action*="criar_senha_final"]', 'senha', 'senha_confirm');
    checkPasswords('form[action*="enviar_nova_senha"]', 'nova_senha', 'confirma_senha');
}


/**
 * -----------------------------------------------------------------
 * 3. Máscaras de Input (IMask.js)
 * -----------------------------------------------------------------
 * [REQUERIMENTO!] Adicione esta linha ao <head> dos seus HTMLs
 * que usam máscaras (abrir-conta, transferência, etc.):
 * * <script src="https://unpkg.com/imask"></script>
 * * [NOTA!] Para máscaras de dinheiro funcionarem, o input DEVE SER
 * type="text", e NÃO type="number".
 */
function initInputMasks() {
    if (typeof IMask === 'undefined') {
        console.warn('Biblioteca IMask.js não foi carregada. Máscaras não serão aplicadas.');
        return;
    }

    // Máscara de CPF
    document.querySelectorAll('input[name="cpf"], input[name="cpf_cnpj_destino"]').forEach(el => {
        IMask(el, { mask: '000.000.000-00' });
    });

    // Máscara de CEP
    document.querySelectorAll('input[name="cep"]').forEach(el => {
        IMask(el, { mask: '00000-000' });
    });

    // Máscara de Telefone
    document.querySelectorAll('input[name="telefone"]').forEach(el => {
        IMask(el, { mask: '(00) 00000-0000' });
    });

    // Máscara de Dinheiro (Salário, Patrimônio, Valor de Transferência)
    const moneyFields = [
        'input[name="salario"]',
        'input[name="vl_patrimonio"]',
        'input[name="valor"]' // campo de transferência
    ];
    document.querySelectorAll(moneyFields.join(', ')).forEach(el => {
        // Altera o tipo para 'text' para a máscara funcionar
        if (el.type === 'number') {
            el.type = 'text';
            el.inputMode = 'decimal';
        }
        
        IMask(el, {
            mask: 'R$ num',
            blocks: {
                num: {
                    mask: Number,
                    scale: 2, // 2 casas decimais
                    thousandsSeparator: '.',
                    padFractionalZeros: true,
                    normalizeZeros: true,
                    radix: ',', // Separador decimal
                    mapToRadix: ['.']
                }
            }
        });
    });
}


/**
 * -----------------------------------------------------------------
 * 4. Preenchimento automático de Endereço (ViaCEP)
 * -----------------------------------------------------------------
 * Usado em: abrir-conta-endereco.html
 */
function initCepAutofill() {
    const cepField = document.querySelector('input[name="cep"]');
    if (!cepField) return; // Se não está na pág de endereço, sai

    // Função auxiliar para travar/destravar campos
    const setAddressFields = (loading, clear = false) => {
        const fields = [
            'input[name="rua"]',
            'input[name="bairro"]',
            'input[name="cidade"]',
            'select[name="estado"]'
        ];
        
        fields.forEach(selector => {
            const field = document.querySelector(selector);
            if (field) {
                field.disabled = loading;
                if (loading) field.value = 'Buscando...';
                if (clear) field.value = '';
            }
        });
    };

    // Adiciona o evento "blur" (quando o usuário sai do campo)
    cepField.addEventListener('blur', () => {
        const cep = cepField.value.replace(/\D/g, ''); // Remove não-números (traço, etc.)
        
        if (cep.length !== 8) return; // CEP inválido

        setAddressFields(true); // Trava os campos e mostra "Buscando..."
        
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    setAddressFields(false, true); // Destrava e limpa
                    cepField.setCustomValidity('CEP não encontrado.');
                } else {
                    // Sucesso! Preenche os campos
                    document.querySelector('input[name="rua"]').value = data.logradouro;
                    document.querySelector('input[name="bairro"]').value = data.bairro;
                    document.querySelector('input[name="cidade"]').value = data.localidade;
                    document.querySelector('select[name="estado"]').value = data.uf;
                    
                    setAddressFields(false, false); // Destrava os campos
                    cepField.setCustomValidity('');
                    document.querySelector('input[name="numero"]').focus(); // Pula para o campo "número"
                }
            })
            .catch(error => {
                console.error('Erro ao buscar CEP:', error);
                setAddressFields(false, true); // Destrava e limpa em caso de erro
            });
    });
}


/**
 * -----------------------------------------------------------------
 * 5. Ligação com o Backend (AJAX/Fetch)
 * -----------------------------------------------------------------
 * Exemplo de como enviar um formulário sem recarregar a página.
 * Usado em: Modal de "Cadastrar Chave PIX" (dashboard-pix.html)
 */
function initAjaxPixModal() {
    // Seleciona o formulário do modal
    const pixForm = document.querySelector('form[action="/pix/cadastrar"]');
    if (!pixForm) return;

    pixForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Impede o envio normal (que recarrega a página)

        const formData = new FormData(pixForm);
        const button = pixForm.querySelector('button[type="submit"]');
        const originalButtonText = button.innerHTML;
        
        // Feedback de "carregando"
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Cadastrando...';

        // Usando a API Fetch para enviar os dados
        fetch(pixForm.action, {
            method: 'POST',
            body: formData,
            headers: { 
                // O Flask (e outros) usa isso para saber que é um AJAX
                'X-Requested-With': 'XMLHttpRequest' 
            }
        })
        .then(response => response.json()) // Espera uma resposta JSON do backend
        .then(data => {
            // Sucesso! O backend deve retornar:
            // { status: 'success', message: 'Chave cadastrada!' }
            if (data.status === 'success') {
                alert(data.message);
                // Solução simples: recarrega a página para mostrar a nova chave na lista
                window.location.reload(); 
            } else {
                // Se o backend retornar um erro de lógica
                // { status: 'error', message: 'Chave já existe' }
                throw new Error(data.message);
            }
        })
        .catch(error => {
            // Erro de rede ou erro lançado acima
            console.error('Erro ao cadastrar chave:', error);
            alert(`Erro: ${error.message}`);
        })
        .finally(() => {
            // Restaura o botão em caso de sucesso ou erro
            button.disabled = false;
            button.innerHTML = originalButtonText;
        });
    });
}

/**
 * NOTA PARA O BACKEND (FLASK)
 * --------------------------
 * Para a função 'initAjaxPixModal' funcionar, sua rota Flask
 * deve retornar JSON em vez de redirecionar.
 *
 * Exemplo em 'conta_routes.py':
 *
 * from flask import jsonify
 *
 * @conta_routes.route('/pix/cadastrar', methods=['POST'])
 * def cadastrar_chave_pix():
 * # (Sua lógica de serviço para salvar a chave...)
 * * if (not request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
 * # Se não for AJAX, faz o fluxo normal
 * flash('Chave cadastrada!')
 * return redirect(url_for('...'))
 *
 * # Se for AJAX (do nosso JS), retorna JSON
 * if (erro_logica):
 * return jsonify({
 * 'status': 'error', 
 * 'message': 'Esta chave já está em uso.'
 * }), 400
 * * return jsonify({
 * 'status': 'success', 
 * 'message': 'Chave PIX cadastrada com sucesso!'
 * })
 *
 */