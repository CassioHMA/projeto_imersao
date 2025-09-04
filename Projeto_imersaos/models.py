from django.db import models

class Cadastro(models.Model):
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    locacao = models.CharField(max_length=200)
    contato = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.nome + " - " + str(self.idade)  + " - " + self.locacao + " - " + self.contato
# Create your models here.
