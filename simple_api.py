from contextlib import contextmanager
import json
import logging
import websocket

from aiohttp import web
from uuid import uuid4
from server import PromptServer

log = logging.getLogger(__name__)


@contextmanager
def connect_ws(client_id="simple_api"):
    ws = websocket.WebSocket()
    ws.connect("ws://{url}/ws?clientId={client_id}".format(url='127.0.0.1', client_id=client_id))
    try:
        yield ws
    finally:
        ws.close()


async def prompt_output(ws, prompt_id):
    output = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                log.debug(data)
                output.update(data)
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break # Execution is done
        else:
            log.warning(f"Non string data received")
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue #previews are binary data

    """
    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output
    """
    return output


@PromptServer.instance.routes.post("/simple")
async def get_hello(request):
    data = await request.post()
    prompt_request =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    client_id = request.header('comfy-user') or str(uuid4())
    with connect_ws(client_id) as ws:
        prompt_request = json.loads(request.urlopen(request).read())  # Can we use .json instead ?
        prompt_id = prompt_request['prompt_id']
        result = await prompt_output(ws, prompt_id)
        log.info(f"Prompt {prompt_id} finished")
        log.debug(result)
        return web.json_response(result)


NODE_CLASS_MAPPINGS = {
}

NODE_DISPLAY_NAME_MAPPINGS = {
}
