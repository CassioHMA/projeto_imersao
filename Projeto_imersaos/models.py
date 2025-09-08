from django.db import models
from django.utils import timezone

class usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + self.email + " - " + self.senha
    
class Cadastro(models.Model):
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    locacao = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + str(self.idade)  + " - " + self.locacao + " - " + self.contato
    
class colaboradores(models.Model):
    nome = models.CharField(max_length=200)
    setor = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + self.setor + " - " + self.contato

class Equipamentos(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome + " - " + str(self.produto.nome) + " - " + str(self.data_emprestimo)
    
class Emprestimos(models.Model):
    produto = models.ForeignKey(Equipamentos, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nome} alugou {self.equipamento.nome} em {self.data_emprestimo}"
    def marcar_devolucao(self):
        self.data_devolucao = timezone.now()
        self.save() 
    def esta_devolvido(self):
        return self.data_devolucao is not None  

class historico_emprestimo(models.Model):
    aluguel = models.ForeignKey(Emprestimos, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    descricao_alteracao = models.TextField()

    def __str__(self):
        return f"Alteração em {self.aluguel} em {self.data_alteracao}"   

