// JavaScript personalizado para o Sistema Financeiro

// Função para formatar valores monetários
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Função para mostrar notificações
function mostrarNotificacao(mensagem, tipo = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Função para validar formulários
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required]');
    
    for (let input of inputs) {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            return false;
        } else {
            input.classList.remove('is-invalid');
        }
    }
    
    return true;
}

// Função para limpar formulários
function limparFormulario(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.value = '';
        input.classList.remove('is-invalid');
    });
}

// Função para confirmar exclusão
function confirmarExclusao(mensagem = 'Tem certeza que deseja excluir este item?') {
    return confirm(mensagem);
}

// Função para carregar dados via AJAX
async function carregarDados(url, opcoes = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...opcoes.headers
            },
            ...opcoes
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        mostrarNotificacao('Erro ao carregar dados. Tente novamente.', 'danger');
        throw error;
    }
}

// Função para enviar dados via AJAX
async function enviarDados(url, dados, metodo = 'POST') {
    try {
        const response = await fetch(url, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });
        
        const resultado = await response.json();
        
        if (!response.ok) {
            throw new Error(resultado.message || 'Erro na requisição');
        }
        
        return resultado;
    } catch (error) {
        console.error('Erro ao enviar dados:', error);
        mostrarNotificacao(error.message, 'danger');
        throw error;
    }
}

// Função para deletar item
async function deletarItem(url, id, callback) {
    if (!confirmarExclusao()) {
        return;
    }
    
    try {
        const resultado = await enviarDados(`${url}/${id}`, {}, 'DELETE');
        mostrarNotificacao(resultado.message, 'success');
        
        if (callback) {
            callback();
        } else {
            location.reload();
        }
    } catch (error) {
        // Erro já tratado na função enviarDados
    }
}

// Função para inicializar tooltips do Bootstrap
function inicializarTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Função para inicializar popovers do Bootstrap
function inicializarPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Inicializar componentes quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    inicializarTooltips();
    inicializarPopovers();
    
    // Adicionar animação aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// Função para exportar dados (futura implementação)
function exportarDados(formato = 'csv') {
    mostrarNotificacao('Funcionalidade de exportação será implementada em breve.', 'info');
}

// Função para imprimir relatórios
function imprimirRelatorio() {
    window.print();
}

// Função para gerar gráficos (futura implementação)
function gerarGraficos() {
    mostrarNotificacao('Gráficos interativos serão implementados em breve.', 'info');
}
