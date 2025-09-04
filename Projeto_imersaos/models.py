from django.db import models

class Cadastro(models.Model):
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    locacao = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + str(self.idade)  + " - " + self.locacao + " - " + self.contato

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome + " - " + str(self.preco) + " - " + str(self.estoque)
    
class Aluguel(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    data_aluguel = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nome} alugou {self.produto.nome} em {self.data_aluguel}"
