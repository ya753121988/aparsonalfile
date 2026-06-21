from aiohttp import web
import aiohttp_jinja2
import jinja2
from config import Config
from database import db

routes = web.RouteTableDef()

# এটিই হলো হেলথ চেক লজিক
@routes.get("/", allow_head=True)
async def home(request):
    return web.Response(text="Bot is Running High!", content_type="text/html")

@routes.get("/watch/{file_id}")
async def watch_handler(request):
    file_id = request.match_info['file_id']
    watermark_text = await db.get_watermark()
    
    context = {
        "file_id": file_id,
        "file_name": f"File_{file_id}",
        "stream_url": f"{Config.URL}/dl/{file_id}",
        "bot_username": Config.BOT_USERNAME,
        "watermark": watermark_text
    }
    return aiohttp_jinja2.render_template('watch.html', request, context)

@routes.get("/dl/{file_id}")
async def dl_handler(request):
    return web.Response(text="Streaming logic ready...")

async def web_server():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.add_routes(routes)
    return app
