from django.test import TestCase
from Projeto_imersaos.models import Colaborador

class ColaboradorModelTest(TestCase):
    
    def setUp(self):
        """Prepara os dados que serão usados no teste."""
        self.colaborador_data = {
            'nome': 'Everton',
            'cpf': '123.456.789-00',
            'cargo': 'Lixeiro',
            'setor': 'Limpeza'
            # O campo 'ativo' usa o valor padrão (True), então não precisamos defini-lo aqui.
        }

    def test_criar_colaborador(self):
        """Testa a criação de um objeto Colaborador."""
        colaborador = Colaborador.objects.create(**self.colaborador_data)
        
        # Verifica se os dados foram salvos corretamente
        self.assertEqual(colaborador.nome, self.colaborador_data['nome'])
        self.assertEqual(colaborador.cpf, self.colaborador_data['cpf'])
        self.assertEqual(colaborador.cargo, self.colaborador_data['cargo'])
        self.assertEqual(colaborador.setor, self.colaborador_data['setor'])
        self.assertTrue(colaborador.ativo)

    def test_str_representation(self):
        """Testa a representação em string do modelo Colaborador."""
        colaborador = Colaborador.objects.create(**self.colaborador_data)
        self.assertEqual(str(colaborador), f"{self.colaborador_data['nome']} - {self.colaborador_data['setor']}")

