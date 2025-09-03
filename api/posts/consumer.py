import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.posts import Post


class PostConsumer(AsyncWebsocketConsumer):
    @classmethod
    def get_room_name(cls, post_id: int) -> str:
        return f"post_{post_id}"

    async def connect(self):
        post_id = self.scope["url_route"]["kwargs"]["post_id"]
        self.room_group_name = PostConsumer.get_room_name(post_id)

        post = await sync_to_async(lambda: Post.objects.filter(id=post_id).first())()

        if not post:
            await self.close()

            return


        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def comment_created(self, event):
        await self.send(text_data=json.dumps(event))