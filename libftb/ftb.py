__author__ = 'Arkan'

import urllib.request
import os.path
import time
import xml.etree.ElementTree as ET

import libftb.internal.parser as parser

CDN_ROOT = "http://ftb.cursecdn.com/FTB2"


def get_packs():
    root = __get_or_create_cache()
    return parser.packs_xml_to_dict(root)


def get_pack_url(pack_dict, version=None, server=False):
    """
    :type version str
    :type server bool
    """
    pack_id = pack_dict['id']
    if not version:
        version = pack_dict['version']
    version.replace('.', '_')
    print("Getting URL for ID {} ({}) (server: {})".format(pack_id, version, server))

    if server:
        file = pack_dict['server_url']
    else:
        file = pack_dict['url']

    return __get_pack_url(pack_id, version, file)


def __get_or_create_cache():
    if not (os.path.isfile('modpacks.xml') and (time.time() - os.path.getmtime('modpacks.xml')) < 3600):
        print("Updating local copy of modpacks.xml...")
        urllib.request.urlretrieve(__get_static_url('modpacks.xml'), 'modpacks.xml')
    return ET.parse('modpacks.xml').getroot()


def __get_static_url(file):
    return "{}/static/{}".format(CDN_ROOT, file)


def __get_pack_url(pack, version, file):
    return "{}/modpacks/{}/{}/{}".format(CDN_ROOT, pack, version, file)