from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)  # Armazenar senha com hash
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):  
        return f"{self.nome} - {self.email}"
    
    
class Colaborador(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    setor = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

    def __str__(self):  
        return f"{self.nome} - {self.setor}"
    
class Equipamento(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Equipamento')
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço (R$)')
    estoque = models.IntegerField(verbose_name='Quantidade em Estoque', default=0)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    
    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
class EmprestimoEquipamento(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('em_atraso', 'Em Atraso'),
        ('devolvido', 'Devolvido'), 
    ]
    # Usar PROTECT para evitar a exclusão de equipamentos/colaboradores com histórico de empréstimo.
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    data_devolucao_prevista = models.DateTimeField(null=True, blank=True, verbose_name='Devolução Prevista')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_emprestimo'] # Ordena pelos mais recentes por padrão

    def __str__(self):
        return f"{self.colaborador.nome} - {self.equipamento.nome} ({self.get_status_display()})"

    def marcar_devolucao(self):
        """Marca um empréstimo como devolvido, atualiza o status, a data e o estoque do equipamento."""
        if self.status == 'devolvido':
            return # Evita processamento desnecessário

        self.data_devolucao = timezone.now()
        self.status = 'devolvido'
        self.equipamento.estoque += 1
        self.equipamento.save()
        self.save(update_fields=['data_devolucao', 'status'])

    @property
    def esta_devolvido(self):
        """Retorna True se o empréstimo já foi devolvido."""
        return self.status == 'devolvido'
 
    
