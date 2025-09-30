document.addEventListener('DOMContentLoaded', function() {
    const tabelaColaboradoresBody = document.getElementById('tabela-colaboradores-body');

    // Executa o código dos Colaboradores apenas se a tabela existir
    if (tabelaColaboradoresBody) {
        const formColaborador = document.getElementById('form-colaborador');
        const formColaboradorData = document.getElementById('form-colaborador-data');
        const novoColaboradorBtn = document.getElementById('novo-colaborador');
        const cancelarColaboradorBtn = document.getElementById('cancelar-colaborador');

        // Função para carregar colaboradores
        function carregarColaboradores() {
            fetch('/api/colaboradores/')
                .then(response => response.json())
                .then(data => {
                    tabelaColaboradoresBody.innerHTML = '';
                    if (data.length === 0) {
                        tabelaColaboradoresBody.innerHTML = '<tr><td colspan="7" class="text-center">Nenhum colaborador cadastrado.</td></tr>';
                    } else {
                        data.forEach(colaborador => {
                            const row = `
                                <tr>
                                    <td>${colaborador.id}</td>
                                    <td>${colaborador.nome}</td>
                                    <td>${colaborador.cpf}</td>
                                    <td>${colaborador.matricula}</td>
                                    <td>${colaborador.cargo}</td>
                                    <td>${colaborador.setor}</td>
                                    <td>
                                        <button class="btn-icon btn-edit" title="Editar" onclick="editarColaborador(${colaborador.id})">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn-icon btn-delete" title="Excluir" onclick="confirmarExclusaoColaborador(${colaborador.id})">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            `;
                            tabelaColaboradoresBody.innerHTML += row;
                        });
                    }
                });
        }

        // Função para abrir o formulário para novo colaborador
        novoColaboradorBtn.addEventListener('click', function() {
            formColaborador.style.display = 'block';
            document.getElementById('titulo-form-colaborador').textContent = 'Novo Colaborador';
            formColaboradorData.reset();
            document.getElementById('colaborador-id').value = '';
        });

        // Função para cancelar
        cancelarColaboradorBtn.addEventListener('click', function() {
            formColaborador.style.display = 'none';
        });

        // Função para editar colaborador
        window.editarColaborador = function(id) {
            fetch(`/api/colaboradores/${id}/`)
                .then(response => response.json())
                .then(data => {
                    formColaborador.style.display = 'block';
                    document.getElementById('titulo-form-colaborador').textContent = 'Editar Colaborador';
                    document.getElementById('colaborador-id').value = data.id;
                    document.getElementById('colaborador-nome').value = data.nome;
                    document.getElementById('colaborador-cpf').value = data.cpf;
                    document.getElementById('colaborador-matricula').value = data.matricula;
                    document.getElementById('colaborador-cargo').value = data.cargo;
                    document.getElementById('colaborador-setor').value = data.setor;
                });
        }

        // Função para confirmar exclusão de colaborador
        window.confirmarExclusaoColaborador = function(id) {
            if (confirm('Tem certeza que deseja excluir este colaborador?')) {
                fetch(`/api/colaboradores/${id}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    if (response.ok) {
                        carregarColaboradores();
                    }
                });
            }
        }

        // Submissão do formulário
        formColaboradorData.addEventListener('submit', function(e) {
            e.preventDefault();
            const id = document.getElementById('colaborador-id').value;
            const url = id ? `/api/colaboradores/${id}/` : '/api/colaboradores/';
            const method = id ? 'PUT' : 'POST';

            const formData = {
                nome: document.getElementById('colaborador-nome').value,
                cpf: document.getElementById('colaborador-cpf').value,
                matricula: document.getElementById('colaborador-matricula').value,
                cargo: document.getElementById('colaborador-cargo').value,
                setor: document.getElementById('colaborador-setor').value,
            };

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    carregarColaboradores();
                    formColaborador.style.display = 'none';
                } else {
                    // Handle errors
                    console.error(data);
                }
            });
        });

        // Carregar colaboradores ao carregar a página
        carregarColaboradores();
    }

    // Função para pegar o CSRF token (usada por ambas as seções)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Função para confirmar exclusão de equipamento
    window.confirmarExclusaoEquipamento = function(deleteUrl) {
        if (confirm("Você tem certeza que deseja excluir este equipamento?")) {
            let form = document.createElement('form');
            form.method = 'POST';
            form.action = deleteUrl;

            let csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = getCookie('csrftoken');
            form.appendChild(csrfInput);

            document.body.appendChild(form);
            form.submit();
        }
    }
});