document.addEventListener('DOMContentLoaded', function() {
    // A lógica de manipulação do DOM para colaboradores foi removida
    // pois a funcionalidade agora é gerenciada pelo fluxo tradicional do Django.

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