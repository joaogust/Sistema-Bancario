/*
 * Este arquivo contém todas as interações de JavaScript
 * para o front-end da aplicação.
 *
 * Funções:
 * 1. Ativação da Validação do Bootstrap
 * 2. Confirmação de Senha em tempo real
 * 3. Máscaras de Input (CPF, CEP, Dinheiro, etc.)
 * 4. Preenchimento automático de Endereço (ViaCEP)
 * 5. Envio de formulário AJAX (Ex: Modal PIX)
 * 6. Sistema de Transferências PIX/TED
 * 7. Toggle de Saldo
 *
 */

document.addEventListener('DOMContentLoaded', () => {
    initBootstrapValidation();
    initPasswordConfirmation();
    initInputMasks();
    initCepAutofill();
    initAjaxPixModal();
    initToggleSaldo();
    initTransferencias();
    initConfirmacaoTransferencia();
    console.log('IFSP scripts carregados com sucesso.');
});

function initTransferencias() {
    const valorInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    valorInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
    const formPix = document.getElementById('formPix');
    if (formPix) {
        formPix.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validarFormularioPIX(this)) {
                return;
            }
            
            await processarTransferenciaPIX(this);
        });
    }
    const formTed = document.getElementById('formTed');
    if (formTed) {
        formTed.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validarFormularioTED(this)) {
                return;
            }
            
            await processarTransferenciaTED(this);
        });
    }
    const pixValor = document.getElementById('pixValor');
    if (pixValor) {
        pixValor.addEventListener('input', function() {
            validarValorPIX(this);
        });
    }
    const tedValor = document.getElementById('tedValor');
    if (tedValor) {
        tedValor.addEventListener('input', function() {
            validarValorTED(this);
        });
    }
    const tedCpfCnpj = document.getElementById('tedCpfCnpj');
    if (tedCpfCnpj) {
        tedCpfCnpj.addEventListener('blur', function() {
            validarCpfCnpj(this);
        });
    }
}

function validarFormularioPIX(form) {
    const chave = form.querySelector('#pixChave').value.trim();
    const valorInput = form.querySelector('#pixValor');
    const valor = parseFloat(valorInput.value);
    const senha = form.querySelector('#pixSenha').value.trim();
    if (!chave) {
        mostrarErroTransferencia('Por favor, informe a chave PIX.');
        return false;
    }
    if (!valor || isNaN(valor) || valor <= 0) {
        mostrarErroTransferencia('Por favor, informe um valor válido.');
        return false;
    }
    if (valor > 5000) {
        mostrarErroTransferencia('Valor máximo para PIX é R$ 5.000,00.');
        return false;
    }
    if (!senha) {
        mostrarErroTransferencia('Por favor, informe sua senha.');
        return false;
    }
    if (!validarChavePIX(chave)) {
        mostrarErroTransferencia('Chave PIX inválida. Verifique o formato.');
        return false;
    }
    return true;
}

function validarValorPIX(input) {
    const valor = parseFloat(input.value);
    if (valor > 5000) {
        input.setCustomValidity('Valor máximo para PIX é R$ 5.000,00');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
}

function validarChavePIX(chave) {
    chave = chave.replace(/\s+/g, '').toLowerCase();
    if (/^\d{11}$/.test(chave)) {
        return true;
    }
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(chave)) {
        return true;
    }
    if (/^55\d{10,11}$/.test(chave) || /^\d{10,11}$/.test(chave)) {
        return true;
    }
    if (/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/.test(chave)) {
        return true;
    }
    return chave.length >= 5;
}

function validarFormularioTED(form) {
    const banco = form.querySelector('#tedBanco').value;
    const agencia = form.querySelector('#tedAgencia').value.trim();
    const conta = form.querySelector('#tedConta').value.trim();
    const tipoConta = form.querySelector('#tedTipoConta').value;
    const nome = form.querySelector('#tedNome').value.trim();
    const cpfCnpj = form.querySelector('#tedCpfCnpj').value.trim();
    const valorInput = form.querySelector('#tedValor');
    const valor = parseFloat(valorInput.value);
    const senha = form.querySelector('#tedSenha').value.trim();
    if (!banco) {
        mostrarErroTransferencia('Por favor, selecione o banco.');
        return false;
    }
    if (!agencia) {
        mostrarErroTransferencia('Por favor, informe a agência.');
        return false;
    }
    if (!conta) {
        mostrarErroTransferencia('Por favor, informe o número da conta.');
        return false;
    }
    if (!tipoConta) {
        mostrarErroTransferencia('Por favor, selecione o tipo de conta.');
        return false;
    }
    if (!nome) {
        mostrarErroTransferencia('Por favor, informe o nome do destinatário.');
        return false;
    }
    if (!cpfCnpj) {
        mostrarErroTransferencia('Por favor, informe o CPF/CNPJ do destinatário.');
        return false;
    }
    if (!valor || isNaN(valor) || valor < 1) {
        mostrarErroTransferencia('Valor mínimo para TED é R$ 1,00.');
        return false;
    }
    if (!senha) {
        mostrarErroTransferencia('Por favor, informe sua senha.');
        return false;
    }
    if (!validarCpfCnpj(cpfCnpj)) {
        mostrarErroTransferencia('CPF/CNPJ inválido.');
        return false;
    }
    return true;
}

function validarValorTED(input) {
    const valor = parseFloat(input.value);
    if (valor < 1) {
        input.setCustomValidity('Valor mínimo para TED é R$ 1,00');
        input.classList.add('is-invalid');
    } else {
        input.setCustomValidity('');
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
}

function validarCpfCnpj(input) {
    const valor = input.value.replace(/\D/g, '');
    if ((valor.length === 11 || valor.length === 14)) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        return false;
    }
}

async function processarTransferenciaPIX(form) {
    const btn = form.querySelector('button[type="submit"]');
    const spinner = btn.querySelector('.spinner-border');    
    try {
        btn.disabled = true;
        spinner.classList.remove('d-none');      
        const formData = new FormData(form);
        const response = await fetch('/conta/realizar-transferencia-pix', {
            method: 'POST',
            body: formData
        });       
        const resultado = await response.json();
        if (resultado.sucesso) {
            window.location.href = '/conta/transferencia/concluida';
        } else {
            mostrarErroTransferencia(resultado.mensagem);
        }
    } catch (error) {
        console.error('Erro na transferência PIX:', error);
        mostrarErroTransferencia('Erro de conexão. Tente novamente.');
    } finally {
        btn.disabled = false;
        spinner.classList.add('d-none');
    }
}

async function processarTransferenciaTED(form) {
    const btn = form.querySelector('button[type="submit"]');
    const spinner = btn.querySelector('.spinner-border');
    try {
        btn.disabled = true;
        spinner.classList.remove('d-none');
        const formData = new FormData(form);
        const response = await fetch('/conta/realizar-transferencia-ted', {
            method: 'POST',
            body: formData
        });
        const resultado = await response.json();
        if (resultado.sucesso) {
            window.location.href = '/conta/transferencia/concluida';
        } else {
            mostrarErroTransferencia(resultado.mensagem);
        }
    } catch (error) {
        console.error('Erro na transferência TED:', error);
        mostrarErroTransferencia('Erro de conexão. Tente novamente.');
    } finally {
        btn.disabled = false;
        spinner.classList.add('d-none');
    }
}

function mostrarErroTransferencia(mensagem) {
    const alertContainer = document.querySelector('.pt-3.pb-2.mb-3');
    if (alertContainer) {
        const alertasExistentes = alertContainer.querySelectorAll('.alert');
        alertasExistentes.forEach(alerta => alerta.remove());
        const alertHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ${mensagem}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        alertContainer.insertAdjacentHTML('afterbegin', alertHTML);
    } else {
        alert('Erro: ' + mensagem);
    }
}

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

function initPasswordConfirmation() {
    const checkPasswords = (formSelector, passName, confirmName) => {
        const form = document.querySelector(formSelector);
        if (!form) return;
        const passField = form.querySelector(`input[name="${passName}"]`);
        const confirmField = form.querySelector(`input[name="${confirmName}"]`);
        if (!passField || !confirmField) return; 
        const validate = () => {
            if (passField.value !== confirmField.value) {
                confirmField.setCustomValidity('As senhas não conferem.');
                confirmField.classList.add('is-invalid');
            } else {
                confirmField.setCustomValidity('');
                confirmField.classList.remove('is-invalid');
                confirmField.classList.add('is-valid');
            }
        };
        passField.addEventListener('input', validate);
        confirmField.addEventListener('input', validate);
    };
    checkPasswords('form[action*="criar_senha_final"]', 'senha', 'senha_confirm');
    checkPasswords('form[action*="enviar_nova_senha"]', 'nova_senha', 'confirma_senha');
}

function initInputMasks() {
    if (typeof IMask === 'undefined') {
        console.warn('Biblioteca IMask.js não foi carregada. Máscaras não serão aplicadas.');
        return;
    }
    document.querySelectorAll('input[name="cpf"], input[name="cpf_cnpj_destino"]').forEach(el => {
        IMask(el, { mask: '000.000.000-00' });
    });
    document.querySelectorAll('input[name="cep"]').forEach(el => {
        IMask(el, { mask: '00000-000' });
    });
    document.querySelectorAll('input[name="telefone"]').forEach(el => {
        IMask(el, { mask: '(00) 00000-0000' });
    });
    const moneyFields = [
        'input[name="salario"]',
        'input[name="vl_patrimonio"]',
        'input[name="valor"]' // campo de transferência
    ];
    document.querySelectorAll(moneyFields.join(', ')).forEach(el => {
        if (el.type === 'number') {
            el.type = 'text';
            el.inputMode = 'decimal';
        }
        IMask(el, {
            mask: 'R$ num',
            blocks: {
                num: {
                    mask: Number,
                    scale: 2,
                    thousandsSeparator: '.',
                    padFractionalZeros: true,
                    normalizeZeros: true,
                    radix: ',',
                    mapToRadix: ['.']
                }
            }
        });
    });
}

function initCepAutofill() {
    const cepField = document.querySelector('input[name="cep"]');
    if (!cepField) return;
    const setAddressFields = (loading, clear = false) => {
        const fields = [
            'input[name="rua"]',
            'input[name="bairro"]',
            'input[name="cidade"]',
            'select[name="estado"]',
            'input[name="estado"]'
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
    cepField.addEventListener('blur', () => {
        const cep = cepField.value.replace(/\D/g, '');
        if (cep.length !== 8) return;
        setAddressFields(true);
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta da API');
                }
                return response.json();
            })
            .then(data => {
                if (data.erro) {
                    setAddressFields(false, true);
                    cepField.setCustomValidity('CEP não encontrado.');
                    cepField.classList.add('is-invalid');
                } else {
                    document.querySelector('input[name="rua"]').value = data.logradouro || '';
                    document.querySelector('input[name="bairro"]').value = data.bairro || '';
                    document.querySelector('input[name="cidade"]').value = data.localidade || '';
                    const estadoSelect = document.querySelector('select[name="estado"]');
                    const estadoInput = document.querySelector('input[name="estado"]');
                    if (estadoSelect) {
                        estadoSelect.value = data.uf || '';
                    } else if (estadoInput) {
                        estadoInput.value = data.uf || '';
                    }
                    setAddressFields(false, false);
                    cepField.setCustomValidity('');
                    cepField.classList.remove('is-invalid');
                    cepField.classList.add('is-valid');
                    const numeroField = document.querySelector('input[name="numero"]');
                    if (numeroField) numeroField.focus();
                }
            })
            .catch(error => {
                console.error('Erro ao buscar CEP:', error);
                setAddressFields(false, true);
                cepField.setCustomValidity('Erro ao buscar CEP.');
                cepField.classList.add('is-invalid');
            });
    });
}

function initAjaxPixModal() {
    const pixForm = document.querySelector('form[action="/pix/cadastrar"]');
    if (!pixForm) return;
    pixForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(pixForm);
        const button = pixForm.querySelector('button[type="submit"]');
        const originalButtonText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Cadastrando...';
        fetch(pixForm.action, {
            method: 'POST',
            body: formData,
            headers: { 
                'X-Requested-With': 'XMLHttpRequest' 
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta do servidor');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                window.location.reload();
            } else {
                throw new Error(data.message);
            }
        })
        .catch(error => {
            console.error('Erro ao cadastrar chave:', error);
            alert(`Erro: ${error.message}`);
        })
        .finally(() => {
            button.disabled = false;
            button.innerHTML = originalButtonText;
        });
    });
}

function initToggleSaldo() {
    const btn = document.getElementById('btn-toggle-saldo');
    const saldoEl = document.getElementById('saldo-valor');
    if (!btn || !saldoEl) return;
    const saldoOriginal = saldoEl.getAttribute('data-saldo');
    let saldoEstaVisivel = true;
    btn.addEventListener('click', () => {
        if (saldoEstaVisivel) {
            saldoEl.textContent = 'R$ ●●●●●,●●';
            btn.innerHTML = '<i class="bi bi-eye"></i> Mostrar';
            saldoEstaVisivel = false;
        } else {
            saldoEl.textContent = `R$ ${saldoOriginal}`;
            btn.innerHTML = '<i class="bi bi-eye-slash"></i> Ocultar';
            saldoEstaVisivel = true;
        }
    });
}

function initConfirmacaoTransferencia() {
    const formConfirmarPix = document.getElementById('formConfirmarPix');
    if (formConfirmarPix) {
        formConfirmarPix.addEventListener('submit', function(e) {
            validarFormularioConfirmacao(e, this, 'btnConfirmarPix');
        });
    }
    const formConfirmarTed = document.getElementById('formConfirmarTed');
    if (formConfirmarTed) {
        formConfirmarTed.addEventListener('submit', function(e) {
            validarFormularioConfirmacao(e, this, 'btnConfirmarTed');
        });
    }
    const senhaInput = document.getElementById('senha_transacao');
    if (senhaInput) {
        senhaInput.focus();
    }
}

function validarFormularioConfirmacao(event, form, botaoId) {
    event.preventDefault();
    const senhaInput = form.querySelector('#senha_transacao');
    const senha = senhaInput.value.trim();
    if (!senha) {
        mostrarErro('Por favor, digite sua senha.');
        senhaInput.focus();
        return false;
    }
    if (senha.length < 4) {
        mostrarErro('A senha deve ter pelo menos 4 caracteres.');
        senhaInput.focus();
        return false;
    }
    const botao = document.getElementById(botaoId);
    const textoOriginal = botao.innerHTML;
    botao.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processando...';
    botao.disabled = true;
    const timeoutId = setTimeout(() => {
        botao.innerHTML = textoOriginal;
        botao.disabled = false;
        mostrarErro('Tempo limite excedido. Tente novamente.');
    }, 10000);
    botao.setAttribute('data-timeout-id', timeoutId);
    form.submit();
}

function mostrarErro(mensagem) {
    const alertContainer = document.querySelector('main .px-md-4');
    if (alertContainer) {
        const alertasExistentes = alertContainer.querySelectorAll('.alert.alert-danger');
        alertasExistentes.forEach(alerta => alerta.remove());
        const alertHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle-fill"></i> ${mensagem}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        alertContainer.insertAdjacentHTML('afterbegin', alertHTML);
    } else {
        alert('Erro: ' + mensagem);
    }
}

function removerLoadingBotao(botaoId) {
    const botao = document.getElementById(botaoId);
    if (botao) {
        const textoOriginal = botao.getAttribute('data-original-text');
        if (textoOriginal) {
            botao.innerHTML = textoOriginal;
        } else {
            if (botaoId === 'btnConfirmarPix') {
                botao.innerHTML = '<i class="bi bi-check-circle"></i> Confirmar Transferência PIX';
            } else if (botaoId === 'btnConfirmarTed') {
                botao.innerHTML = '<i class="bi bi-check-circle"></i> Confirmar Transferência TED';
            }
        }
        botao.disabled = false;
        const timeoutId = botao.getAttribute('data-timeout-id');
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
    }
}

window.IFSPBank = {
    validarFormularioPIX,
    validarFormularioTED,
    processarTransferenciaPIX,
    processarTransferenciaTED,
    mostrarErroTransferencia,
    initConfirmacaoTransferencia,
    validarFormularioConfirmacao,
    mostrarErro,
    removerLoadingBotao
};