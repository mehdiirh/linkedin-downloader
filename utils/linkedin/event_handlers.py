from linkedin_messaging.api_objects import RealTimeEventStreamEvent

from telethon.sync import TelegramClient

from utils.event_objects import EventDetails, TabBadges
from utils.linkedin.tools import authenticate, extract_media


async def handle_message_events(event: RealTimeEventStreamEvent, bot: TelegramClient):
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
            await authenticate(bot, message, uid)

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
