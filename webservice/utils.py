import os
import time


import jwt


def get_jwt():
    app_id = os.getenv("GH_APP_ID")
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id,
    }
    private_key = os.getenv("GH_PRIVATE_KEY")
    encoded = jwt.encode(payload, private_key, algorithm="RS256")
    bearer_token = encoded.decode("utf-8")

    return bearer_token


async def get_installation_access_token(gh, installation_id):
    # doc: https://developer.github.com/v3/apps/#create-a-new-installation-token
    access_token_url = f"/app/installations/{installation_id}/access_tokens"
    jwt = get_jwt()
    response = await gh.post(
        access_token_url,
        data=b"",
        jwt=jwt,
        accept="application/vnd.github.machine-man-preview+json",
    )
    # example response
    # {
    #   "token": "v1.1f699f1069f60xxx",
    #   "expires_at": "2016-07-11T22:14:10Z"
    # }

    return response
