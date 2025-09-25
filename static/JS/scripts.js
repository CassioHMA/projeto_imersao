// static/js/scripts.js

// ==============================================
// CONFIGURAÇÕES E VARIÁVEIS GLOBAIS
// ==============================================
const API_BASE_URL = window.API_BASE_URL || '/api';
const CSRF_TOKEN = window.CSRF_TOKEN;
const USER_PERFIL = window.USER_PERFIL || 'Visualizador';

let currentData = {
    colaboradores: [],
    equipamentos: [],
    emprestimos: [],
    historico: [],
    usuarios: []
};

// Headers padrão para requisições
const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-CSRFToken': CSRF_TOKEN,
};

// ==============================================
// FUNÇÕES DE INICIALIZAÇÃO
// ==============================================

/**
 * Inicializa a aplicação quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthentication();
});

/**
 * Inicializa a aplicação
 */
function initializeApp() {
    // Configura data atual nos formulários
    const today = new Date().toISOString().split('T')[0];
    const dataEmprestimo = document.getElementById('emprestimo-data');
    const dataDevolucao = document.getElementById('emprestimo-data-devolucao');
    
    if (dataEmprestimo) dataEmprestimo.value = today;
    
    if (dataDevolucao) {
        const nextWeek = new Date();
        nextWeek.setDate(nextWeek.getDate() + 7);
        dataDevolucao.value = nextWeek.toISOString().split('T')[0];
    }
    
    // Verifica permissões do usuário
    updateUserPermissions();
    
    // Carrega dados iniciais
    loadInitialData();
}

/**
 * Configura todos os event listeners
 */
function setupEventListeners() {
    // Navegação do menu
    setupMenuNavigation();
    
    // Navegação por abas
    setupTabNavigation();
    
    // Formulários
    setupFormHandlers();
    
    // Botões de ação
    setupActionButtons();
    
    // Modal de confirmação
    setupModalHandlers();
}

/**
 * Verifica se o usuário está autenticado
 */
function checkAuthentication() {
    // Se não há token CSRF, redireciona para login
    if (!CSRF_TOKEN) {
        window.location.href = '/accounts/login/';
    }
}

/**
 * Atualiza as permissões com base no perfil do usuário
 */
function updateUserPermissions() {
    if (USER_PERFIL !== 'Administrador') {
        // Oculta funcionalidades administrativas
        const adminItems = document.querySelectorAll('[data-target="usuarios"], .btn-danger, [onclick*="delete"], [onclick*="excluir"]');
        adminItems.forEach(item => {
            item.style.display = 'none';
        });
    }
    
    if (USER_PERFIL === 'Visualizador') {
        // Apenas visualização - desabilita edição
        const editButtons = document.querySelectorAll('.btn-primary, .btn-success, [onclick*="edit"], [onclick*="editar"], form');
        editButtons.forEach(button => {
            button.style.display = 'none';
        });
    }
}

// ==============================================
// NAVEGAÇÃO E UI
// ==============================================

/**
 * Configura a navegação do menu
 *//**
 * Configuração da navegação do menu
 */
function setupMenuNavigation() {
    // Apenas adiciona comportamento de active aos itens clicados
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault(); // Previne comportamento padrão para links vazios
            }
            
            // Remove active de todos os itens
            document.querySelectorAll('.menu-item').forEach(i => {
                i.classList.remove('active');
            });
            
            // Adiciona active ao item clicado
            this.classList.add('active');
        });
    });
    
    // Destaca o menu atual baseado na URL
    highlightCurrentMenu();
}

/**
 * Destaca o item do menu correspondente à página atual
 */
function highlightCurrentMenu() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    // Remove active de todos os itens primeiro
    menuItems.forEach(item => item.classList.remove('active'));
    
    // Tenta encontrar o item ativo baseado na URL atual
    const currentUrlName = window.CURRENT_URL;
    let activeFound = false;
    
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && href !== '#' && currentUrlName) {
            // Verifica se a URL nomeada corresponde
            if (href.includes(currentUrlName)) {
                item.classList.add('active');
                activeFound = true;
            }
        }
    });
    
    // Fallback: se não encontrou, ativa o dashboard
    if (!activeFound && currentUrlName === 'dashboard') {
        const dashboardItem = document.querySelector('.menu-item[data-target="dashboard"]');
        if (dashboardItem) {
            dashboardItem.classList.add('active');
        }
    }
}

/**
 * Inicializa a aplicação quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
    setupMenuNavigation();
    // ... restante do seu código de inicialização
});

/**
 * Configura a navegação por abas
 */
function setupTabNavigation() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const tabContainer = this.closest('.tabs');
            const tabContent = tabContainer.nextElementSibling;
            
            // Remove classe active de todas as abas
            tabContainer.querySelectorAll('.tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // Adiciona classe active à aba clicada
            this.classList.add('active');
            
            // Esconde todos os conteúdos de abas
            tabContent.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Mostra o conteúdo correspondente
            const targetTab = this.getAttribute('data-tab');
            const targetContent = tabContent.querySelector('#' + targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
                
                // Carrega dados se necessário
                if (targetTab === 'emprestimos-ativos') {
                    loadEmprestimosAtivos();
                } else if (targetTab === 'lista-equipamentos') {
                    loadEquipamentos();
                }
            }
        });
    });
}

/**
 * Alterna para uma seção específica
 */
function switchToSection(section) {
    const menuItem = document.querySelector(`.menu-item[data-target="${section}"]`);
    if (menuItem) {
        menuItem.click();
    }
}

// ==============================================
// CARREGAMENTO DE DADOS
// ==============================================

/**
 * Carrega dados iniciais da aplicação
 */
async function loadInitialData() {
    try {
        await loadDashboardData();
        await loadSelectOptions();
    } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
        showError('Erro ao carregar dados iniciais');
    }
}

/**
 * Carrega dados específicos de cada seção
 */
async function loadSectionData(section) {
    try {
        switch(section) {
            case 'dashboard':
                await loadDashboardData();
                break;
            case 'colaboradores':
                await loadColaboradores();
                break;
            case 'equipamentos':
                await loadEquipamentos();
                break;
            case 'emprestimos':
                await loadEmprestimosAtivos();
                await loadSelectOptions();
                break;
            case 'historico':
                await loadHistorico();
                break;
            case 'usuarios':
                if (USER_PERFIL === 'Administrador') {
                    await loadUsuarios();
                }
                break;
        }
    } catch (error) {
        console.error(`Erro ao carregar dados da seção ${section}:`, error);
        showError(`Erro ao carregar dados da seção ${section}`);
    }
}

/**
 * Função para fazer requisições AJAX
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: { ...defaultHeaders },
        ...options
    };
    
    try {
        showLoading();
        const response = await fetch(url, config);
        
        if (response.status === 403) {
            // Acesso não autorizado
            showError('Acesso não autorizado');
            throw new Error('Acesso não autorizado');
        }
        
        if (response.status === 401) {
            // Não autenticado
            window.location.href = '/accounts/login/';
            throw new Error('Não autenticado');
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        } else {
            return await response.text();
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        showError('Erro ao comunicar com o servidor');
        throw error;
    } finally {
        hideLoading();
    }
}

// ==============================================
// FUNÇÕES DO DASHBOARD
// ==============================================

/**
 * Carrega dados do dashboard
 */
async function loadDashboardData() {
    try {
        const data = await apiRequest('/dashboard/');
        
        // Atualiza os cards
        updateCardValue('total-equipamentos', data.total_equipamentos);
        updateCardValue('total-colaboradores', data.total_colaboradores);
        updateCardValue('emprestimos-ativos', data.emprestimos_ativos);
        updateCardValue('emprestimos-atrasados', data.emprestimos_atrasados);
        
        // Carrega empréstimos recentes
        await loadEmprestimosRecentes();
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
    }
}

/**
 * Atualiza o valor de um card
 */
function updateCardValue(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

/**
 * Carrega empréstimos recentes
 */
async function loadEmprestimosRecentes() {
    try {
        const emprestimos = await apiRequest('/emprestimos/?limit=5');
        currentData.emprestimos = emprestimos;
        renderEmprestimosRecentes(emprestimos);
    } catch (error) {
        console.error('Erro ao carregar empréstimos recentes:', error);
    }
}

/**
 * Renderiza empréstimos recentes na tabela
 */
function renderEmprestimosRecentes(emprestimos) {
    const tbody = document.querySelector('#emprestimos-recentes tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!emprestimos || emprestimos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center">Nenhum empréstimo encontrado</td>
            </tr>
        `;
        return;
    }
    
    emprestimos.forEach(emprestimo => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${emprestimo.colaborador_nome || emprestimo.colaborador}</td>
            <td>${emprestimo.equipamento_nome || emprestimo.equipamento}</td>
            <td>${formatDate(emprestimo.data_emprestimo)}</td>
            <td>${formatDate(emprestimo.data_devolucao_prevista)}</td>
            <td>${getStatusBadge(emprestimo.status)}</td>
        `;
        tbody.appendChild(row);
    });
}

// ==============================================
// FUNÇÕES DE FORMULÁRIO
// ==============================================

/**
 * Configura os handlers dos formulários
 */
function setupFormHandlers() {
    // Formulário de colaborador
    const formColaborador = document.getElementById('form-colaborador-data');
    if (formColaborador) {
        formColaborador.addEventListener('submit', handleColaboradorSubmit);
    }
    
    // Formulário de equipamento
    const formEquipamento = document.getElementById('form-equipamento');
    if (formEquipamento) {
        formEquipamento.addEventListener('submit', handleEquipamentoSubmit);
    }
    
    // Formulário de empréstimo
    const formEmprestimo = document.getElementById('form-emprestimo');
    if (formEmprestimo) {
        formEmprestimo.addEventListener('submit', handleEmprestimoSubmit);
    }
    
    // Formulário de usuário
    const formUsuario = document.getElementById('form-usuario-data');
    if (formUsuario) {
        formUsuario.addEventListener('submit', handleUsuarioSubmit);
    }
}

/**
 * Handler para submit do formulário de colaborador
 */
async function handleColaboradorSubmit(event) {
    event.preventDefault();
    
    const formData = {
        nome: document.getElementById('colaborador-nome').value,
        cpf: document.getElementById('colaborador-cpf').value,
        matricula: document.getElementById('colaborador-matricula').value,
        cargo: document.getElementById('colaborador-cargo').value || null,
        setor: document.getElementById('colaborador-setor').value || null
    };
    
    const colaboradorId = document.getElementById('colaborador-id').value;
    const isEdit = !!colaboradorId;
    
    try {
        let response;
        if (isEdit) {
            response = await apiRequest(`/colaboradores/${colaboradorId}/`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showSuccess('Colaborador atualizado com sucesso!');
        } else {
            response = await apiRequest('/colaboradores/', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showSuccess('Colaborador criado com sucesso!');
        }
        
        hideColaboradorForm();
        await loadColaboradores();
    } catch (error) {
        console.error('Erro ao salvar colaborador:', error);
        showError('Erro ao salvar colaborador');
    }
}

/**
 * Handler para submit do formulário de equipamento
 */
async function handleEquipamentoSubmit(event) {
    event.preventDefault();
    
    const formData = {
        nome: document.getElementById('equipamento-nome').value,
        tipo: document.getElementById('equipamento-tipo').value,
        descricao: document.getElementById('equipamento-descricao').value || null,
        quantidade_total: parseInt(document.getElementById('equipamento-quantidade-total').value),
        quantidade_disponivel: parseInt(document.getElementById('equipamento-quantidade-disponivel').value),
        data_validade: document.getElementById('equipamento-data-validade').value || null
    };
    
    const equipamentoId = document.getElementById('equipamento-id').value;
    const isEdit = !!equipamentoId;
    
    try {
        let response;
        if (isEdit) {
            response = await apiRequest(`/equipamentos/${equipamentoId}/`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showSuccess('Equipamento atualizado com sucesso!');
        } else {
            response = await apiRequest('/equipamentos/', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showSuccess('Equipamento criado com sucesso!');
        }
        
        resetEquipamentoForm();
        await loadEquipamentos();
        await loadSelectOptions(); // Atualiza selects de equipamentos
    } catch (error) {
        console.error('Erro ao salvar equipamento:', error);
        showError('Erro ao salvar equipamento');
    }
}

/**
 * Handler para submit do formulário de empréstimo
 */
async function handleEmprestimoSubmit(event) {
    event.preventDefault();
    
    const formData = {
        colaborador: document.getElementById('emprestimo-colaborador').value,
        equipamento: document.getElementById('emprestimo-equipamento').value,
        data_emprestimo: document.getElementById('emprestimo-data').value,
        data_devolucao_prevista: document.getElementById('emprestimo-data-devolucao').value,
        observacoes: document.getElementById('emprestimo-observacoes').value || null
    };
    
    try {
        const response = await apiRequest('/emprestimos/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showSuccess('Empréstimo registrado com sucesso!');
        document.getElementById('form-emprestimo').reset();
        
        // Atualiza dados
        await loadEmprestimosAtivos();
        await loadDashboardData();
        await loadSelectOptions(); // Atualiza disponibilidade de equipamentos
    } catch (error) {
        console.error('Erro ao registrar empréstimo:', error);
        showError('Erro ao registrar empréstimo');
    }
}

// ==============================================
// FUNÇÕES DE COLABORADORES
// ==============================================

/**
 * Carrega lista de colaboradores
 */
async function loadColaboradores() {
    try {
        const colaboradores = await apiRequest('/colaboradores/');
        currentData.colaboradores = colaboradores;
        renderColaboradores(colaboradores);
    } catch (error) {
        console.error('Erro ao carregar colaboradores:', error);
        showError('Erro ao carregar lista de colaboradores');
    }
}

/**
 * Renderiza colaboradores na tabela
 */
function renderColaboradores(colaboradores) {
    const tbody = document.querySelector('#tabela-colaboradores tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!colaboradores || colaboradores.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">Nenhum colaborador encontrado</td>
            </tr>
        `;
        return;
    }
    
    colaboradores.forEach(colaborador => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${colaborador.id}</td>
            <td>${colaborador.nome}</td>
            <td>${formatCPF(colaborador.cpf)}</td>
            <td>${colaborador.matricula}</td>
            <td>${colaborador.cargo || '-'}</td>
            <td>${colaborador.setor || '-'}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editarColaborador(${colaborador.id})">Editar</button>
                ${USER_PERFIL === 'Administrador' ? 
                    `<button class="btn btn-danger btn-sm" onclick="confirmarExclusaoColaborador(${colaborador.id})">Excluir</button>` : 
                    ''}
            </td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Preenche formulário para editar colaborador
 */
async function editarColaborador(id) {
    try {
        const colaborador = await apiRequest(`/colaboradores/${id}/`);
        
        document.getElementById('colaborador-id').value = colaborador.id;
        document.getElementById('colaborador-nome').value = colaborador.nome;
        document.getElementById('colaborador-cpf').value = colaborador.cpf;
        document.getElementById('colaborador-matricula').value = colaborador.matricula;
        document.getElementById('colaborador-cargo').value = colaborador.cargo || '';
        document.getElementById('colaborador-setor').value = colaborador.setor || '';
        
        document.getElementById('titulo-form-colaborador').textContent = 'Editar Colaborador';
        showColaboradorForm();
    } catch (error) {
        console.error('Erro ao carregar colaborador:', error);
        showError('Erro ao carregar dados do colaborador');
    }
}

/**
 * Mostra formulário de colaborador
 */
function showColaboradorForm() {
    document.getElementById('form-colaborador').style.display = 'block';
}

/**
 * Esconde formulário de colaborador
 */
function hideColaboradorForm() {
    document.getElementById('form-colaborador').style.display = 'none';
    document.getElementById('form-colaborador-data').reset();
    document.getElementById('colaborador-id').value = '';
    document.getElementById('titulo-form-colaborador').textContent = 'Novo Colaborador';
}

/**
 * Confirma exclusão de colaborador
 */
function confirmarExclusaoColaborador(id) {
    showModal(
        'Confirmar Exclusão',
        'Tem certeza que deseja excluir este colaborador? Esta ação não pode ser desfeita.',
        () => excluirColaborador(id)
    );
}

/**
 * Exclui colaborador
 */
async function excluirColaborador(id) {
    try {
        await apiRequest(`/colaboradores/${id}/`, {
            method: 'DELETE'
        });
        
        showSuccess('Colaborador excluído com sucesso!');
        await loadColaboradores();
    } catch (error) {
        console.error('Erro ao excluir colaborador:', error);
        showError('Erro ao excluir colaborador');
    }
}

// ==============================================
// FUNÇÕES DE EQUIPAMENTOS (similar aos colaboradores)
// ==============================================

async function loadEquipamentos() {
    try {
        const equipamentos = await apiRequest('/equipamentos/');
        currentData.equipamentos = equipamentos;
        renderEquipamentos(equipamentos);
    } catch (error) {
        console.error('Erro ao carregar equipamentos:', error);
        showError('Erro ao carregar lista de equipamentos');
    }
}

function renderEquipamentos(equipamentos) {
    const tbody = document.querySelector('#tabela-equipamentos-body');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!equipamentos || equipamentos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">Nenhum equipamento encontrado</td>
            </tr>
        `;
        return;
    }
    
    equipamentos.forEach(equipamento => {
        const row = document.createElement('tr');
        // Lógica para definir o status visualmente
        const statusClass = equipamento.quantidade_disponivel > 0 ? 'status-ativo' : 'status-inativo';
        const statusText = equipamento.quantidade_disponivel > 0 ? 'Disponível' : 'Indisponível';

        row.innerHTML = `
            <td>${equipamento.nome}</td>
            <td>${equipamento.tipo || '-'}</td>
            <td>${equipamento.quantidade_total}</td>
            <td>${equipamento.quantidade_disponivel}</td>
            <td>${equipamento.data_validade ? formatDate(equipamento.data_validade) : '-'}</td>
            <td>
                // Adiciona o status badge, alinhado com o template
                <span class="status-badge ${statusClass}">${statusText}</span>
            </td>
            <td>
                // Adiciona os botões de ação com ícones, alinhados com o template
                <button class="btn-icon btn-edit" title="Editar" onclick="editarEquipamento(${equipamento.id})"><i class="fas fa-edit"></i></button>
                <button class="btn-icon btn-delete" title="Excluir" onclick="confirmarExclusaoEquipamento(${equipamento.id})"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Preenche formulário para editar equipamento
 */
async function editarEquipamento(id) {
    try {
        const equipamento = await apiRequest(`/equipamentos/${id}/`);
        
        document.getElementById('equipamento-id').value = equipamento.id;
        document.getElementById('equipamento-nome').value = equipamento.nome;
        document.getElementById('equipamento-tipo').value = equipamento.tipo || '';
        document.getElementById('equipamento-descricao').value = equipamento.descricao || '';
        document.getElementById('equipamento-quantidade-total').value = equipamento.quantidade_total;
        document.getElementById('equipamento-quantidade-disponivel').value = equipamento.quantidade_disponivel;
        document.getElementById('equipamento-data-validade').value = equipamento.data_validade || '';

        
        document.getElementById('modal-titulo-equipamento').textContent = 'Editar Equipamento';
        showEquipamentoModal();
    } catch (error) {
        console.error('Erro ao carregar equipamento:', error);
        showError('Erro ao carregar dados do equipamento');
    }
}

/**
 * Mostra o modal de equipamento (para criação/edição)
 */
function showEquipamentoModal() {
    document.getElementById('modal-equipamento').style.display = 'block';
}

/**
 * Esconde o modal de equipamento e reseta o formulário
 */
function hideEquipamentoModal() {
    document.getElementById('modal-equipamento').style.display = 'none';
    resetEquipamentoForm(); // Reseta o formulário e limpa o ID oculto
    document.getElementById('modal-titulo-equipamento').textContent = 'Novo Equipamento'; // Reseta o título
}

/**
 * Confirma exclusão de equipamento
 */
function confirmarExclusaoEquipamento(id) {
    showModal( // Usando o modal de confirmação genérico de scripts.js
        'Confirmar Exclusão',
        'Tem certeza que deseja excluir este equipamento? Esta ação não pode ser desfeita.',
        () => excluirEquipamento(id)
    );
}

/**
 * Exclui equipamento
 */
async function excluirEquipamento(id) {
    try {
        await apiRequest(`/equipamentos/${id}/`, {
            method: 'DELETE'
        });
        showSuccess('Equipamento excluído com sucesso!');
        await loadEquipamentos();
        await loadSelectOptions(); // Atualiza selects de equipamentos
    } catch (error) {
        console.error('Erro ao excluir equipamento:', error);
        showError('Erro ao excluir equipamento');
    }
}

// ==============================================
// FUNÇÕES DE EMPRÉSTIMOS
// ==============================================

async function loadEmprestimosAtivos() {
    try {
        const emprestimos = await apiRequest('/emprestimos/');
        currentData.emprestimos = emprestimos;
        renderEmprestimosAtivos(emprestimos);
    } catch (error) {
        console.error('Erro ao carregar empréstimos:', error);
        showError('Erro ao carregar lista de empréstimos');
    }
}

function renderEmprestimosAtivos(emprestimos) {
    const tbody = document.querySelector('#tabela-emprestimos-ativos tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!emprestimos || emprestimos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">Nenhum empréstimo encontrado</td>
            </tr>
        `;
        return;
    }
    
    emprestimos.forEach(emprestimo => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${emprestimo.id}</td>
            <td>${emprestimo.colaborador_nome || emprestimo.colaborador}</td>
            <td>${emprestimo.equipamento_nome || emprestimo.equipamento}</td>
            <td>${formatDate(emprestimo.data_emprestimo)}</td>
            <td>${formatDate(emprestimo.data_devolucao_prevista)}</td>
            <td>${getStatusBadge(emprestimo.status)}</td>
            <td>
                <button class="btn btn-success btn-sm" onclick="registrarDevolucao(${emprestimo.id})">Registrar Devolução</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function registrarDevolucao(emprestimoId) {
    try {
        await apiRequest(`/emprestimos/${emprestimoId}/devolucao/`, {
            method: 'POST'
        });
        
        showSuccess('Devolução registrada com sucesso!');
        await loadEmprestimosAtivos();
        await loadDashboardData();
        await loadSelectOptions(); // Atualiza disponibilidade de equipamentos
    } catch (error) {
        console.error('Erro ao registrar devolução:', error);
        showError('Erro ao registrar devolução');
    }
}

// ==============================================
// FUNÇÕES UTILITÁRIAS
// ==============================================

/**
 * Formata data para formato brasileiro
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

/**
 * Formata CPF
 */
function formatCPF(cpf) {
    if (!cpf) return '-';
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

/**
 * Retorna badge de status
 */
function getStatusBadge(status) {
    const badges = {
        'Em aberto': 'badge-success',
        'Devolvido': 'badge-info',
        'Atrasado': 'badge-warning'
    };
    return `<span class="badge ${badges[status] || 'badge-secondary'}">${status}</span>`;
}

/**
 * Carrega opções para selects
 */
async function loadSelectOptions() {
    await loadColaboradoresSelect();
    await loadEquipamentosSelect();
}

async function loadColaboradoresSelect() {
    try {
        const colaboradores = await apiRequest('/colaboradores/');
        const select = document.getElementById('emprestimo-colaborador');
        if (select) {
            // Mantém a opção selecionada atual
            const currentValue = select.value;
            select.innerHTML = '<option value="">Selecione o colaborador</option>';
            
            colaboradores.forEach(colaborador => {
                const option = document.createElement('option');
                option.value = colaborador.id;
                option.textContent = `${colaborador.nome} (${colaborador.matricula})`;
                select.appendChild(option);
            });
            
            // Restaura a seleção anterior se ainda existir
            if (currentValue) {
                select.value = currentValue;
            }
        }
    } catch (error) {
        console.error('Erro ao carregar colaboradores para select:', error);
    }
}

async function loadEquipamentosSelect() {
    try {
        const equipamentos = await apiRequest('/equipamentos/');
        const select = document.getElementById('emprestimo-equipamento');
        if (select) {
            // Mantém a opção selecionada atual
            const currentValue = select.value;
            select.innerHTML = '<option value="">Selecione o equipamento</option>';
            
            equipamentos.forEach(equipamento => {
                // Mostra apenas equipamentos disponíveis
                if (equipamento.quantidade_disponivel > 0) {
                    const option = document.createElement('option');
                    option.value = equipamento.id;
                    option.textContent = `${equipamento.nome} (${equipamento.quantidade_disponivel} disponíveis)`;
                    option.dataset.disponivel = equipamento.quantidade_disponivel;
                    select.appendChild(option);
                }
            });
            
            // Restaura a seleção anterior se ainda existir
            if (currentValue) {
                select.value = currentValue;
            }
        }
    } catch (error) {
        console.error('Erro ao carregar equipamentos para select:', error);
    }
}

// ==============================================
// FUNÇÕES DE UI/UX
// ==============================================

function showLoading() {
    // Implementar indicador de carregamento se necessário
}

function hideLoading() {
    // Implementar ocultação de indicador de carregamento se necessário
}

function showSuccess(message) {
    showMessage(message, 'success');
}

function showError(message) {
    showMessage(message, 'error');
}

function showMessage(message, type = 'info') {
    // Remove mensagens existentes
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Cria nova mensagem
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.innerHTML = `
        <i>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</i>
        <span>${message}</span>
    `;
    
    // Adiciona ao container de mensagens
    let messagesContainer = document.querySelector('.messages');
    if (!messagesContainer) {
        messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages';
        document.body.appendChild(messagesContainer);
    }
    
    messagesContainer.appendChild(messageDiv);
    
    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function setupModalHandlers() {
    const modal = document.getElementById('modal-confirmacao');
    const confirmBtn = document.getElementById('modal-confirmar');
    const cancelBtn = document.getElementById('modal-cancelar');
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideModal);
    }
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideModal();
            }
        });
    }
}

function showModal(title, message, confirmCallback) {
    const modal = document.getElementById('modal-confirmacao');
    const titleEl = document.getElementById('modal-titulo');
    const messageEl = document.getElementById('modal-mensagem');
    const confirmBtn = document.getElementById('modal-confirmar');
    
    if (modal && titleEl && messageEl && confirmBtn) {
        titleEl.textContent = title;
        messageEl.textContent = message;
        
        // Remove event listeners anteriores
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Adiciona novo event listener
        newConfirmBtn.addEventListener('click', function() {
            if (confirmCallback) confirmCallback();
            hideModal();
        });
        
        modal.style.display = 'flex';
    }
}

function hideModal() {
    const modal = document.getElementById('modal-confirmacao');
    if (modal) {
        modal.style.display = 'none';
    }
}

// ==============================================
// CONFIGURAÇÃO DE BOTÕES DE AÇÃO
// ==============================================

function setupActionButtons() {
    // Botão novo colaborador
    const novoColaboradorBtn = document.getElementById('novo-colaborador');
    if (novoColaboradorBtn) {
        novoColaboradorBtn.addEventListener('click', showColaboradorForm);
    }
    
    // Botão cancelar colaborador
    const cancelarColaboradorBtn = document.getElementById('cancelar-colaborador');
    if (cancelarColaboradorBtn) {
        cancelarColaboradorBtn.addEventListener('click', hideColaboradorForm);
    }
    
    // Botão novo equipamento
    const novoEquipamentoBtn = document.querySelector('[onclick="showEquipamentoModal()"]');
    if (novoEquipamentoBtn) {
        novoEquipamentoBtn.addEventListener('click', function() {
            hideEquipamentoModal(); // Reseta o formulário e o título antes de mostrar
            showEquipamentoModal(); // Mostra o modal
        });
    }

    // Botão cancelar equipamento (dentro do modal)
    const cancelarEquipamentoModalBtn = document.querySelector('#modal-equipamento .btn-secondary');
    if (cancelarEquipamentoModalBtn) {
        cancelarEquipamentoModalBtn.addEventListener('click', hideEquipamentoModal);
    }
    // Botão cancelar equipamento
    const cancelarEquipamentoBtn = document.getElementById('cancelar-equipamento');
    if (cancelarEquipamentoBtn) {
        cancelarEquipamentoBtn.addEventListener('click', resetEquipamentoForm);
    }
    
    // Botão exportar
    const exportarRelatorioBtn = document.getElementById('exportar-relatorio');
    if (exportarRelatorioBtn) {
        exportarRelatorioBtn.addEventListener('click', exportRelatorio);
    }
    
    // Botão filtrar histórico
    const filtrarHistoricoBtn = document.getElementById('filtrar-historico');
    if (filtrarHistoricoBtn) {
        filtrarHistoricoBtn.addEventListener('click', filtrarHistorico);
    }
}

async function exportRelatorio() {
    try {
        const response = await apiRequest('/emprestimos/export/');
        
        // Cria um link para download
        const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'relatorio_emprestimos.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showSuccess('Relatório exportado com sucesso!');
    } catch (error) {
        console.error('Erro ao exportar relatório:', error);
        showError('Erro ao exportar relatório');
    }
}

async function filtrarHistorico() {
    const dataInicio = document.getElementById('historico-data-inicio').value;
    const dataFim = document.getElementById('historico-data-fim').value;
    
    try {
        let url = '/historico/';
        if (dataInicio || dataFim) {
            url += '?';
            if (dataInicio) url += `data_inicio=${dataInicio}`;
            if (dataFim) url += `&data_fim=${dataFim}`;
        }
        
        const historico = await apiRequest(url);
        renderHistorico(historico);
    } catch (error) {
        console.error('Erro ao filtrar histórico:', error);
        showError('Erro ao filtrar histórico');
    }
}

// ==============================================
// OUTRAS FUNÇÕES (implementar conforme necessário)
// ==============================================

async function loadHistorico() {
    // Implementar carregamento do histórico
}

async function loadUsuarios() {
    // Implementar carregamento de usuários
}

function renderHistorico(historico) {
    // Implementar renderização do histórico
}

// Exportar funções globais para uso em onclick
window.editarColaborador = editarColaborador;
window.confirmarExclusaoColaborador = confirmarExclusaoColaborador;
window.registrarDevolucao = registrarDevolucao;
window.editarEquipamento = editarEquipamento; // Exporta a nova função
window.confirmarExclusaoEquipamento = confirmarExclusaoEquipamento; // Exporta a nova função
window.showEquipamentoModal = showEquipamentoModal; // Exporta a nova função
window.hideEquipamentoModal = hideEquipamentoModal; // Exporta a nova função
window.switchToSection = switchToSection;
window.showColaboradorForm = showColaboradorForm;
window.hideColaboradorForm = hideColaboradorForm;
window.resetEquipamentoForm = resetEquipamentoForm; // Garante que está exportada
window.exportRelatorio = exportRelatorio;
window.filtrarHistorico = filtrarHistorico;