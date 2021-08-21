# -*- coding: utf-8 -*-

import sys
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
from datetime import datetime
import re
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
try:
    import json
except:
    import simplejson as json
import base64


if sys.argv[1] == 'SetPassword':
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
    if os.path.exists(addon_data_path)==False:
        os.mkdir(addon_data_path)
    xbmc.sleep(4)
    arquivo = os.path.join(addon_data_path, "password.txt")
    exists = os.path.isfile(arquivo)
    if exists == False:
        password = '0069'
        p_encoded = base64.b64encode(password.encode()).decode('utf-8')
        p_file1 = open(arquivo,'w')
        p_file1.write(p_encoded)
        p_file1.close()
        xbmc.sleep(4)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        ps = dialog.numeric(0, 'Insira a senha atual:')
        if ps == p_file_b64_decode:
            ps2 = dialog.numeric(0, 'Insira a nova senha:')
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    else:
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        ps = dialog.numeric(0, 'Insira a senha atual:')
        if ps == p_file_b64_decode:
            ps2 = dialog.numeric(0, 'Insira a nova senha:')
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão') 
    exit()

addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
profile = xbmc.translatePath(__addon__.getAddonInfo('profile'))
home = xbmc.translatePath(__addon__.getAddonInfo('path'))
fanart_default = os.path.join(home, 'fanart.jpg')
favorites = os.path.join(profile, 'favorites.dat')
username = addon.getSetting('username')
password = addon.getSetting('password')
host = addon.getSetting('server')
stream_format = addon.getSetting('output')


def notify(message,name=False,iconimage=False,timeShown=5000):
    if name and iconimage:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (name, message, timeShown, iconimage))
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, message, timeShown, __icon__))


def addDir(name,url,mode,iconimage,fanart,description,folder=True):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    try:
        if folder:
            li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        else:
            li=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    except:
        li=xbmcgui.ListItem(name)
        if folder:
            li.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})
        else:
            li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})
    if mode == 4:
        li.setProperty('IsPlayable', 'true')        
    li.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', fanart_default)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=li, isFolder=folder)

      
def browser(url):
    try:
        from urllib.request import Request, urlopen, URLError  # Python 3
    except ImportError:
        from urllib2 import Request, urlopen, URLError  # Python 2
    try:
        req = Request(url)
        req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        req.add_header('Purpose', 'prefetch')
        req.add_header('Sec-Fetch-Site', 'same-origin')
        req.add_header('Sec-Fetch-Mode', 'navigate')
        req.add_header('Sec-Fetch-Dest', 'document')
        content = urlopen(req).read().decode('utf-8')
    except URLError as e:
        if hasattr(e, 'code'):
            xbmc.executebuiltin("Notification(Falha, código de erro - "+str(e.code)+",10000,"+__icon__+")")    
        elif hasattr(e, 'reason'):
            xbmc.executebuiltin("Notification(Falha, motivo - "+str(e.reason)+",10000,"+__icon__+")")
        content = ''
    return content        

def info_account():
    try:
        api = '%s/player_api.php?username=%s&password=%s'%(host,username,password)
        api = api.replace('//player_api.php', '/player_api.php')
        data  = browser(api)
        api = json.loads(data)
        auth = api.get('user_info')['auth']
        if int(auth)==1:
            status = api.get('user_info')['status']
            exp_date = api.get('user_info')['exp_date']
            is_trial = api.get('user_info')['is_trial']
            created_at = api.get('user_info')['created_at']
            max_connections = api.get('user_info')['max_connections']
        else:
            status = 'disabled'
            exp_date = ''
            is_trial = ''
            created_at = ''
            max_connections = ''            
        return auth,status,exp_date,is_trial,created_at,max_connections
    except:
        return 0,'disabled','','','',''

def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match
    
def get_m3u8(url):
    notify('Carregando...')
    data = browser(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:-1.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                if not cat in group_list:
                    group_list.append(cat)
                    addDir(cat.encode('utf-8', 'ignore'),url,3,'','','')
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            group_list = []
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    if not cat in group_list:
                        group_list.append(cat)
                        addDir(cat.encode('utf-8', 'ignore'),url,3,'','','')
                else:
                    addDir(channel_name.encode('utf-8', 'ignore'),stream_url,4,thumbnail,'','',folder=False)
            if match2 ==[]:
                notify('Nenhuma lista M3U...')
    else:
        notify('Nenhuma lista M3U...')
                
                
def get_m3u8_2(name,url):
    data = browser(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        content = data.rstrip()      
        match1 = re.compile(r'#EXTINF:-1.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                try:
                    name = name.decode('utf-8')
                except:
                    pass
                if cat == name:
                    addDir(channel_name.encode('utf-8', 'ignore'),stream_url,4,thumbnail,'','',folder=False) 
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    if cat == name:
                        addDir(channel_name.encode('utf-8', 'ignore'),stream_url,4,thumbnail,'','',folder=False)
            if match2 ==[]:
                notify('Nenhuma lista M3U...')
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        notify('Nenhuma lista M3U...')        
        

def vip():
    auth,status,exp_date,is_trial,created_at,max_connections = info_account()
    if int(auth) == 1:
        if int(stream_format) == 0:
            saida_canal = 'm3u8'
        else:
            saida_canal = 'ts'
        stream_vip = '%s/get.php?username=%s&password=%s&type=m3u_plus&output=%s'%(host,username,password,saida_canal)
        stream_vip = stream_vip.replace('//get.php', '/get.php')
        get_m3u8(stream_vip)
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        xbmcaddon.Addon().openSettings()

def time_convert(timestamp):
    try:
        if timestamp > '':
            dt_object = datetime.fromtimestamp(int(timestamp))
            time_br = dt_object.strftime('%d/%m/%Y às %H:%M:%S')
            return str(time_br)
        else:
            valor = ''
            return valor
    except:
        valor = ''
        return valor

def status():
    auth,status,exp_date,is_trial,created_at,max_connections = info_account()
    if status > '' and status == 'Active':
        status_result = 'Ativo'
    else:
        status_result = 'Expirado ou Não existe'
    if exp_date > '':
        expires = time_convert(str(exp_date))
    else:
        expires = ''
    if is_trial > '' and is_trial == '0':
        vip_trial = 'Não'
    else:
        vip_trial = 'Sim'
    if created_at > '':
        created_time = time_convert(str(created_at))
    else:
        created_time = ''
    if max_connections > '':
        limite_conexao = max_connections
    else:
        limite_conexao = ''
    msg = 'Status: [COLOR yellow]%s[/COLOR]\nExpira em: [COLOR yellow]%s[/COLOR]\nDemonstrativo: [COLOR yellow]%s[/COLOR]\nCriado em: [COLOR yellow]%s[/COLOR]\nConexões permitidas: [COLOR yellow]%s[/COLOR]'%(status_result,str(expires),vip_trial,str(created_time),str(limite_conexao))
    xbmcgui.Dialog().textviewer('Conta Premium:', msg)        
    
                        


def play_video(name, url, iconimage):
    try:
        li = xbmcgui.ListItem(name, path=url, iconImage=iconimage, thumbnailImage=iconimage)
    except:
        li = xbmcgui.ListItem(name, path=url)
        li.setArt({"icon": iconimage, "thumb": iconimage})
    li.setInfo(type='video', infoLabels={'Title': name, 'plot': ''})
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


def parental_password():
    try:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        arquivo = os.path.join(addon_data_path, "password.txt")
        exists = os.path.isfile(arquivo)
        if exists == False:
            password = '0069'
            p_encoded = base64.b64encode(password.encode()).decode('utf-8')
            p_file = open(arquivo,'w')
            p_file.write(p_encoded)
            p_file.close()
    except:
        pass


def home():
    addDir('[B]Entrar[/B]','',2,'','','')
    addDir('[B]Status[/B]','',5,'','','')
    addDir('[B]Configurações[/B]','',1,'','','')    
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
    

def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param



def main():
    params=get_params()
    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=None
    
    xbmcplugin.setContent(addon_handle, 'movies')

    try:
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name=urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        mode=int(params["mode"])
    except:
        pass
    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        description=urllib.unquote_plus(params["description"])
    except:
        pass

    if mode==None:
        parental_password()
        home()
    elif mode==1:
        xbmcaddon.Addon().openSettings()
    elif mode==2:
        vip()
    elif mode==3:
        if re.search("Adult",name,re.IGNORECASE) or re.search("A Casa das Brasileirinhas",name,re.IGNORECASE):
            addonID = xbmcaddon.Addon().getAddonInfo('id')
            addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
            arquivo = os.path.join(addon_data_path, "password.txt")
            p_file = open(arquivo,'r+')
            p_file_read = p_file.read()
            p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
            dialog = xbmcgui.Dialog()
            ps = dialog.numeric(0, 'Insira a senha atual:')
            if ps == p_file_b64_decode:
                get_m3u8_2(name,url)
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
                xbmcplugin.endOfDirectory(addon_handle)
        else:
            get_m3u8_2(name,url)            
    elif mode==4:
        play_video(name, url, iconimage)
    elif mode==5:
        status()
       

if __name__ == "__main__":
	main()