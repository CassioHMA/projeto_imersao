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

class equipamento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome + " - " + str(self.produto.nome) + " - " + str(self.data_emprestimo)
    
class emprestimo(models.Model):
    status_choices = [
        ('ativo', 'ativo'),
        ('em atraso', 'em atraso'),
        ('devolvido', 'devolvido'), 
    ]
    equipamento = models.ForeignKey(equipamento, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(cadastro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='ativo')   

    def __str__(self):
        return f"{self.colaborador.nome} alugou {self.equipamento.nome} em {self.data_emprestimo}"
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

