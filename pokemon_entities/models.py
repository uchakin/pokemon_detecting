from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название стихии')
    avatar = models.ImageField(verbose_name='Картинка стихии', upload_to='Type', null=True, blank=True)
    strong_against = models.ManyToManyField(
        'self', verbose_name='Силен против', blank=True, related_name='pokemon_entities', symmetrical=False)

    def __str__(self):
        return f"{self.title}"


class Pokemon(models.Model):
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на английском')
    title_ru = models.CharField(max_length=200, blank=True, verbose_name='Название на русском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название на японском')
    img = models.ImageField(verbose_name='Картинка покемона')
    description = models.TextField(max_length=400, blank=True, verbose_name='Описание покемона')
    element_type = models.ManyToManyField(
        PokemonElementType, related_name='pokemons', blank=True, verbose_name='Стихия покемона')
    previous_evolution = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='next_evolutions',
        verbose_name='Предыдущая эволюция')

    def __str__(self):
        return f"{self.title_en}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='pokemon_entities')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Дата и время появления', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Дата и время удалениия с карты', null=True)
    level = models.IntegerField(verbose_name='Уровень покемона', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True)
