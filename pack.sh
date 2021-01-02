#!/bin/bash

echo -n '{"package": "vimove", "name": "vi like movements", "mod": ' > manifest.json
date +%s >> manifest.json
echo '}' >> manifest.json
zip vimove.ankiaddon ./*py manifest.json
