"""
    Taken from https://github.com/MikeSiLVO/script.skinshortcuts
    Copyright (C) 2013-2021 Skin Shortcuts (script.skinshortcuts)
    This file is part of script.skinshortcuts
    SPDX-License-Identifier: GPL-2.0-only
    See LICENSES/GPL-2.0-only.txt for more information.
"""

from kodi_six import xbmc
import json


def rpc_request(request):
    payload = xbmc.executeJSONRPC(json.dumps(request))
    return json.loads(payload)


def validate_rpc_response(response, request=None, required_attrib=None):
    if 'result' in response:
        if not required_attrib:
            return True
        if required_attrib in response['result'] and response['result'][required_attrib]:
            return True

    if 'error' in response:
        message = response['error']['message']
        code = response['error']['code']
        error = (
            f'JSONRPC: Requested |{request}| received error |{message}| and code: |{code}|'
            if request
            else f'JSONRPC: Received error |{message}| and code: |{code}|'
        )
    elif request:
        error = f'JSONRPC: Requested |{request}| received error |{str(response)}|'
    else:
        error = f'JSONRPC: Received error |{str(response)}|'

    xbmc.log(error, xbmc.LOGERROR)
    return False


def get_settings():
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "Settings.getSettings"
    }

    response = rpc_request(payload)
    if not validate_rpc_response(response, payload, 'settings'):
        return None
    return response


def debug_show_log_info(value):
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "Settings.setSettingValue",
        "params": {
            "setting": "debug.showloginfo",
            "value": value
        }
    }

    response = rpc_request(payload)
    return None if not validate_rpc_response(response, payload) else response


def toggle_debug():
    settings = get_settings()
    if not settings:
        return False

    result = [x['value'] for x in settings['result']['settings'] if x['id'] == 'debug.showloginfo'][0]
    togglevar = not result
    debug_show_log_info(togglevar)
    return True
