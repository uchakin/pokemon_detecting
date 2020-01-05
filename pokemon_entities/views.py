import folium
import branca

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def make_url(pokemon, request):
    return request.build_absolute_uri(pokemon.img.url)


def add_pokemon(folium_map, lat, lon, name, pokemon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(image_url, icon_size=(50, 50),)
    html = f"""
        <h4>{pokemon.pokemon}</h4>
        <p>
        <b>Уровень</b>: {pokemon.level}<br>
        <b>Здоровье</b>: {pokemon.health}<br>
        <b>Сила</b>: {pokemon.strength}<br>
        <b>Защита</b>: {pokemon.defence}<br>
        <b>Выносливость</b>: {pokemon.stamina}<br>
        </p>
        """
    iframe = branca.element.IFrame(html=html, width=180, height=160)
    popup = folium.Popup(iframe)
    folium.Marker([lat, lon], tooltip=name, icon=icon, popup=popup).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        img = make_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
                    pokemon_entity.pokemon.title_en, pokemon_entity, img)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append(
            {
            'pokemon_id': pokemon.id,
            'img': pokemon.img.url,
            'title_ru': pokemon.title_en,
            }
        )

    return render(
        request,
        "mainpage.html",
        context={'map': folium_map._repr_html_(), 'pokemons': pokemons_on_page,})


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    try:
        requested_pokemon = Pokemon.objects.prefetch_related('pokemon_entities').get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if requested_pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'title_ru': requested_pokemon.previous_evolution.title_ru,
            'img': requested_pokemon.previous_evolution.img.url
        }
    else:
        previous_evolution = None

    try:
        next_pokemon = requested_pokemon.next_evolutions.all()[0]
        next_evolution = {
            'pokemon_id': next_pokemon.id,
            'title_ru': next_pokemon.title_ru,
            'img': next_pokemon.img.url
        }
    except IndexError:
        next_evolution = None

    elements = requested_pokemon.element_type.all()
    elements_types = []
    for element in elements:
        image = element.avatar.url
        elements_types.append({
            'title': element.title,
            'img': image,
            'strong_against': element.strong_against.all()
        })

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img': requested_pokemon.img.url,
        'description': requested_pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
        'element_type': elements_types
    }

    for pokemon_entity in PokemonEntity.objects.all():
        img = make_url(pokemon_entity.pokemon, request)
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru,
            pokemon_entity,
            img
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon
                                                    })
