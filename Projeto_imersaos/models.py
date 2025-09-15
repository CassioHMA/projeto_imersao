from django.db import models
from django.utils import timezone

class usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + self.email + " - " + self.senha
    
class cadastro(models.Model):
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    locacao = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + str(self.idade)  + " - " + self.locacao + " - " + self.contato
    
class colaborador(models.Model):
    nome = models.CharField(max_length=200)
    setor = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + self.setor + " - " + self.contato
    
class Equipamentos(models.Model):
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
    
class emprestimo(models.Model):
    status_choices = [
        ('ativo', 'ativo'),
        ('em atraso', 'em atraso'),
        ('devolvido', 'devolvido'), 
    ]
    produto = models.ForeignKey(Equipamentos, on_delete=models.CASCADE)  # ← Use 'produto' aqui
    colaborador = models.ForeignKey(colaborador, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='ativo') 

    def __str__(self):
        return f"{self.colaborador.nome} - {self.produto.nome}" 

    def __str__(self):
        return f"{self.colaborador.nome} alugou {self.produto.nome} em {self.data_emprestimo}"
    def marcar_devolucao(self):
        self.data_devolucao = timezone.now()
        self.save() 
    def esta_devolvido(self):
        return self.data_devolucao is not None  

class historico_emprestimo(models.Model):
    emprestimo = models.ForeignKey(emprestimo, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    descricao_alteracao = models.TextField()

    def __str__(self):
        return f"Alteração em {self.emprestimo} em {self.data_alteracao}"   
    

