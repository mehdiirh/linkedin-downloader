from utils.linkedin.tools import extract_media, authenticate

from linkedin_messaging import ChallengeException, LinkedInMessaging
from linkedin_messaging.api_objects import RealTimeEventStreamEvent

from utils.event_objects import EventDetails

from pathlib import Path
import asyncio
import logging
import re
import json

cookie_path = Path(__file__).parent.joinpath("cookies.pickle")
config_path = Path(__file__).resolve().parent.parent.parent / 'config.json'

config = json.load(open(config_path, 'r'))["LINKEDIN"]
username = config["USER"]
password = config["PASS"]

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)


async def listen(bot):
    """
    Listen to events from the LinkedIn direct messages

    Args:
        bot (telethon.TelegramClient): Telegram client
    """

    print('Start listening to linkedin messages...')

    messaging = LinkedInMessaging()

    if cookie_path.exists():
        with open(cookie_path, "rb") as cf:
            messaging = LinkedInMessaging.from_pickle(cf.read())

    if not await messaging.logged_in():
        try:
            await messaging.login(username, password)
        except ChallengeException:
            await messaging.enter_2fa(input("Enter 2FA Code: "))

        with open(cookie_path, "wb+") as cf:
            cf.write(messaging.to_pickle())

    async def auth(code, linkedin_id):
        if re.match(r'^\d+:\w+$', code):
            await authenticate(bot, code, linkedin_id)

    async def on_event(event: RealTimeEventStreamEvent):

        media = {
            'images': [],
            'videos': [],
            'documents': [],
        }
        event_details = {
            'text': '',
            'sender': '',
            'author': '',
            'media': media
        }

        if (e := event.event) and (ec := e.event_content):

            uid = e.from_.messaging_member.mini_profile.entity_urn.id_parts[0]

            if not (me := ec.message_event):
                return

            if message := me.attributed_body.text:
                await auth(message, uid)

            if not (fu := me.feed_update) or not (content := fu.content):
                return

            event_details['author'] = fu.actor.name.text

            event_details['sender'] = e.from_.messaging_member.mini_profile.entity_urn.id_parts[0]

            if fu.commentary and fu.commentary.text:
                event_details['text'] = fu.commentary.text.text

            if (im_component := content.image_component) and (images := im_component.images):
                for im in images:
                    for attr in im.attributes:
                        artifact = max(
                            attr.vector_image.artifacts,
                            key=lambda x: x.width
                        )
                        media['images'].append(
                            attr.vector_image.root_url + artifact.file_identifying_url_path_segment
                        )

            if (video_component := content.video_component) and \
                    (videos := video_component.video_play_metadata.progressive_streams):
                best_resolution = max(
                    videos,
                    key=lambda x: x.size
                )
                media['videos'].append({
                    'url': best_resolution.streaming_locations[0].url,
                    'format': best_resolution.media_type
                })

            if document := content.document_component:
                media['documents'].append(document.document.transcribed_document_url)

            await extract_media(bot, EventDetails.from_dict(event_details))

    messaging.add_event_listener("event", on_event)
    task = asyncio.create_task(messaging.start_listener())

    # wait basically forever
    await asyncio.sleep(2 ** 128)

    await asyncio.gather(task)

    await messaging.close()
