import math
import mimetypes
from aiohttp import web
import aiohttp_jinja2
import jinja2
from config import Config
from database import db

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def home(request):
    return web.Response(text="Bot is Live and Optimized!")

@routes.get("/watch/{file_id}")
async def watch_handler(request):
    file_id = request.match_info['file_id']
    wm = await db.get_watermark()
    context = {
        "file_id": file_id,
        "stream_url": f"{Config.URL}/dl/{file_id}",
        "bot_username": Config.BOT_USERNAME,
        "watermark": wm
    }
    return aiohttp_jinja2.render_template('watch.html', request, context)

@routes.get("/dl/{file_id}")
async def stream_handler(request):
    file_id = int(request.match_info['file_id'])
    bot = request.app['bot']
    
    range_header = request.headers.get("Range", 0)
    
    try:
        msg = await bot.get_messages(Config.FILE_STORE_ID, file_id)
        media = msg.document or msg.video or msg.audio
        file_size = media.file_size
        
        # Range Request handling
        from_bytes = 0
        if range_header:
            from_bytes = int(range_header.replace("bytes=", "").split("-")[0])
        
        headers = {
            "Content-Type": media.mime_type or 'application/octet-stream',
            "Content-Length": str(file_size - from_bytes),
            "Content-Range": f"bytes {from_bytes}-{file_size-1}/{file_size}",
            "Accept-Ranges": "bytes",
        }

        return web.Response(
            status=206 if range_header else 200,
            headers=headers,
            body=bot.stream_media(media, offset=from_bytes)
        )
    except Exception as e:
        return web.Response(text=str(e), status=404)

async def web_server(bot_instance):
    app = web.Application()
    app['bot'] = bot_instance
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.add_routes(routes)
    return app
