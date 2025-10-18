from django.test import TestCase
from .model import Equipamento

class EquipamentoModelTest(TestCase):
    def test_str_representation(self):
        
def test_criar_funcionario(self):
        """Testa a criação de um colaborador com todos os campos"""
        Colaboradores = Colaboradores.objetos.create(**self.Colaboradores)  # CORRIGIDO: objetos
        
        self.assertEqual(Colaboradores.nome, 'João')
        self.assertEqual(Colaboradores.cpf, '123.456.789-00')
        self.assertEqual(Colaboradores.cargo, 'Engenheiro')
        self.assertEqual(Colaboradores.setor, 'Engenharia')
        self.assertTrue(Colaboradores.ativo, 'ativo')
        


        