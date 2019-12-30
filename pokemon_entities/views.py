import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def make_url(pokemon, request):
    return request.build_absolute_uri(pokemon.img_url.url)


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        img_url = make_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
                    pokemon_entity.pokemon.title_en, img_url)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.img_url.url,
            'title_ru': pokemon.title_en,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    try:
        requested_pokemon = Pokemon.objects.prefetch_related('pokemon_entity').get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if requested_pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'title_ru': requested_pokemon.previous_evolution.title_ru,
            'img_url': requested_pokemon.previous_evolution.img_url.url
        }
    else:
        previous_evolution = ''

    try:
        next_pokemon = requested_pokemon.next_evolution.all()[0]
        next_evolution = {
            'pokemon_id': next_pokemon.id,
            'title_ru': next_pokemon.title_ru,
            'img_url': next_pokemon.img_url.url
        }
    except IndexError:
        next_evolution = ''

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': requested_pokemon.img_url.url,
        'description': requested_pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    for pokemon_entity in PokemonEntity.objects.all():
        img_url = make_url(pokemon_entity.pokemon, request)
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.pokemon.title_ru,
            img_url
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon
                                                    })
