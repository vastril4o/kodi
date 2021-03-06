import xbmc
import xbmcaddon

import json

import api_debug
import api_data
import api_login
import api_iostream

_addon = xbmcaddon.Addon()
_user = _addon.getSetting('settings_username')
_password = _addon.getSetting('settings_password')
_files_path = _addon.getSetting('settings_files_path')
_iptv_simple_reload = _addon.getSetting('settings_iptv_simple_reload')
_download_epg = _addon.getSetting('settings_epg')

if not _user or not _password or not _files_path:
    api_debug.show_notifycation('Settings empty')
    _addon.openSettings()
else:
    api_debug.show_progress()
    
    # login
    session = api_login.login(_user, _password)
    api_debug.update_progress(20)

    # load data
    # channel session 2h
    if api_iostream.load_channel() == False:
        json_channel = api_data.get_channel(session)
        api_iostream.save_channel(json_channel)
        api_debug.update_progress(40)
    
        # epg
        if _download_epg == 'true':
            json_epg = api_data.get_epg(json_channel)
            api_iostream.save_epg(json_epg)
            api_debug.update_progress(60)
            
    api_debug.update_progress(100)
    api_debug.close_progress()
    
    if _iptv_simple_reload == 'true':
        # reset iptv simple
        jsonIPTVtoggle = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":"toggle"},"id":1}'
        
        xbmc.executeJSONRPC(jsonIPTVtoggle)
        xbmc.sleep(1000)
        xbmc.executeJSONRPC(jsonIPTVtoggle)
