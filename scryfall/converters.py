from scryfall.models import Card, Expansion


def card_from_json(json: dict) -> Card:
    try:
        oracle_text = json.get('oracle_text', None)
        if oracle_text is None:
            if 'card_faces' in json.keys():
                faces = json['card_faces']
                faces_text = [face['oracle_text'] for face in faces]
                oracle_text = '\n//\n'.join(faces_text)
            else:
                oracle_text = 'Error parsing oracle text'
        return Card(
            name=json['name'],
            image_url=json["image_uris"]["normal"],
            source_url=json["scryfall_uri"].split('?')[0],
            mana_cost=json['mana_cost'],
            type_line=json['type_line'],
            oracle_text=oracle_text,
            power=json.get('power', None),
            toughness=json.get('toughness', None),
            scryfall_id=json['id']
        )
    except KeyError as error:
        print(f'Error parsing: ' + str(json))
        print(error)
        raise


def expansion_from_json(json: dict) -> Expansion:
    try:
        return Expansion(
            name=json['name'],
            code=json['code'],
            scryfall_id=json['id']
        )
    except KeyError as error:
        print(f'Error parsing: ' + str(json))
        print(error)
        raise
