import logging
import sys

from scryfall.models import Card, Expansion

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def card_from_json(json: dict) -> Card:
    try:
        oracle_text = json.get('oracle_text', None)
        image_uri = ""
        try:
            image_uri = json["image_uris"]["normal"]
        except KeyError as e:
            pass
        if oracle_text is None:
            if 'card_faces' in json.keys():
                faces = json['card_faces']
                faces_text = [face['oracle_text'] for face in faces]
                oracle_text = '\n//\n'.join(faces_text)
                try:
                    image_uri = json['card_faces'][0]["image_uris"]["normal"]
                except KeyError as e:
                    logger.error(e)
            else:
                oracle_text = 'Error parsing oracle text'
        return Card(
            name=json['name'],
            image_url=image_uri,
            source_url=json["scryfall_uri"].split('?')[0],
            mana_cost=json['mana_cost'],
            type_line=json['type_line'],
            oracle_text=oracle_text,
            power=json.get('power', None),
            toughness=json.get('toughness', None),
            scryfall_id=json['id']
        )
    except KeyError as error:
        logger.debug(f'Error parsing: ' + str(json))
        logger.error(error)
        raise


def expansion_from_json(json: dict) -> Expansion:
    try:
        return Expansion(
            name=json['name'],
            code=json['code'],
            scryfall_id=json['id'],
            released_at=json['released_at'],
            set_type=json['set_type']
        )
    except KeyError as error:
        logger.debug(f'Error parsing: ' + str(json))
        logger.error(error)
        raise
