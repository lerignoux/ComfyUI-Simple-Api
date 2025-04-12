# ComfyUI-Simple-Api
A simple http api for comfy. Enables to get generation results directly without relying on a websocket connection

The `api/simple` route will take
* json data containting a single 'prompt' parameter containing the ComfyUI workflow. similar to what comfy sends as prompt
* an optional header 'comfy.UserId' if you want your generation to be linked with a specific comfy user.

## Usage:
### python
```python
import request

with open("example/workflow.json") as f:
    workflow = json.load(f)

outputs = request.post("localhost:8188/api/simple", workflow):

```

### js
```js

```

### C#
```C#

```
