from django.db.models import IntegerChoices


class Priority(IntegerChoices):
    LOWEST = 11, "Baixíssima"
    LOW = 22, "Baixa"
    MEDIUM = 33, "Média"
    HIGHT  = 44, "Alta"
    HIGHEST = 55, "Altíssima"
