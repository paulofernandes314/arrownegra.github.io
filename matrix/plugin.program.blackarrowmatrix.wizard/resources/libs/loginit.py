################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['youtube', 'multiweather', 'netflix', 'pvriptvsimple', 'opensubsbyopensubs']

LOGINID = {
    'youtube': {
        'name'     : '[B]***Youtube API Keys***[/B]',
        'saved'    : 'youtube',
        'plugin'   : 'plugin.video.youtube',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'youtube_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.youtube', 'settings.xml'),
        'default'  : 'youtube.api.key',
        'data'     : ['youtube.api.key', 'youtube.api.last.hash', 'youtube.api.id', 'youtube.api.secret'],
        'activate' : ''},
		
    'multiweather': {
        'name'     : '[B]***Multi-Weather Weather***[/B]',
        'plugin'   : 'weather.multi',
        'saved'    : 'multiweather',
        'path'     : os.path.join(CONFIG.ADDONS, 'weather.multi'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'weather.multi', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'weather.multi', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'multiweather_location'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'weather.multi', 'settings.xml'),
        'default'  : 'loc1',
        'data'     : ['loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc1id', 'loc2id', 'loc3id', 'loc4id', 'loc5id'],
        'activate' : ''},

    'netflix': {
        'name'     : '[B]***Netflix***[/B]',
        'plugin'   : 'plugin.video.netflix',
        'saved'    : 'netflix',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix', 'resources/media/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix', 'resources/media/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'netflix_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.netflix', 'settings.xml'),
        'default'  : 'email',
        'data'     : ['email', 'password'],
        'activate' : ''},			
		
    'pvriptvsimple': {
        'name'     : '[B]***Kodi IPTV Simple Client PVR***[/B]',
        'plugin'   : 'pvr.iptvsimple',
        'saved'    : 'pvriptvsimple',
        'path'     : os.path.join(CONFIG.ADDONS, 'pvr.iptvsimple'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'pvr.iptvsimple', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'pvr.iptvsimple', 'icon.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'pvriptvsimple_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'pvr.iptvsimple', 'settings.xml'),
        'default'  : 'm3uUrl',
        'data'     : ['epgUrl', 'logoBaseUrl', 'm3uUrl', 'userAgent'],
        'activate' : ''},
		
    'opensubsbyopensubs': {
        'name'     : '[B]***OpenSubtitles By OpenSubtitles***[/B]',
        'plugin'   : 'service.subtitles.opensubtitles_by_opensubtitles',
        'saved'    : 'opensubtitles',
        'path'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_logo_512x512.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'opensubsbyopensubs_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'service.subtitles.opensubtitles_by_opensubtitles', 'settings.xml'),
        'default'  : 'OSuser',
        'data'     : ['OSuser', 'OSpass'],
        'activate' : ''}

}


def login_user(who):
    user = None
    if LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            try:
                add = tools.get_addon_by_id(LOGINID[who]['plugin'])
                user = add.getSetting(LOGINID[who]['default'])
            except:
                pass
    return user


def login_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.LOGINFOLD):
        os.makedirs(CONFIG.LOGINFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(LOGINID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(LOGINID[log]['plugin'])
                    default = LOGINID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_login(do, log)
                except:
                    pass
            else:
                logging.log('[Login Info] {0}({1}) is not installed'.format(LOGINID[log]['name'], LOGINID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('loginnextsave', tools.get_date(days=3, formatted=True))
    else:
        if LOGINID[who]:
            if os.path.exists(LOGINID[who]['path']):
                update_login(do, who)
        else:
            logging.log('[Login Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for login in LOGINID:
            clear_saved(login,  True)
    elif LOGINID[who]:
        file = LOGINID[who]['file']
        if os.path.exists(file):
            os.remove(file)
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, LOGINID[who]['name']),
                               '[COLOR {0}]Login Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               LOGINID[who]['icon'])
        CONFIG.set_setting(LOGINID[who]['saved'], '')
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_login(do, who):
    file = LOGINID[who]['file']
    settings = LOGINID[who]['settings']
    data = LOGINID[who]['data']
    addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
    saved = LOGINID[who]['saved']
    default = LOGINID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = LOGINID[who]['name']
    icon = LOGINID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    login = ElementTree.SubElement(root, 'login')
                    id = ElementTree.SubElement(login, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(login, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Login Data Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Login Data] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Login Data Click To Authorize {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('login'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                    
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Login Data Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Login Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Login Data Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings), level=xbmc.LOGDEBUG)
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Trakt Data] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in LOGINID:
            if os.path.exists(LOGINID[log]['path']):
                auto_update(log)
    elif LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            u = login_user(who)
            su = CONFIG.get_setting(LOGINID[who]['saved'])
            n = LOGINID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                login_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Login Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n)
                                    +'\n'+"Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u)
                                    +'\n'+"Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
                    login_it('update', who)
            else:
                login_it('update', who)


def import_list(who):
    if who == 'all':
        for log in LOGINID:
            if os.path.exists(LOGINID[log]['file']):
                import_list(log)
    elif LOGINID[who]:
        if os.path.exists(LOGINID[who]['file']):
            file = LOGINID[who]['file']
            addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
            saved = LOGINID[who]['saved']
            default = LOGINID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = LOGINID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('login'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Login Data: Imported![/COLOR]'.format(CONFIG.COLOR2))


def activate_login(who):
    if LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            act = LOGINID[who]['activate']
            addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
            if act == '':
                addonid.openSettings()
            else:
                xbmc.executebuiltin(LOGINID[who]['activate'])
        else:
            dialog = xbmcgui.Dialog()

            dialog.ok(CONFIG.ADDONTITLE, '{0} is not currently installed.'.format(LOGINID[who]['name']))
    else:
        xbmc.executebuiltin('Container.Refresh()')
        return

    check = 0
    while not login_user(who) or login_user(who) == "":
        if check == 30:
            break
        check += 1
        time.sleep(10)
    xbmc.executebuiltin('Container.Refresh()')
