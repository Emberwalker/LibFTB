__author__ = 'Arkan'


def packs_xml_to_dict(root):
    """
    :type root xml.etree.Element
    """
    packs = list(root)
    out = {}
    for p in packs:
        mods = p.get('mods')
        old_vers = p.get('oldVersions')

        mods_str, old_str = ("", "")
        if mods:
            mods_str = mods.split('; ')  # FTB y u no have seperate mod tags?
        if old_vers:
            old_str = old_vers.split(';')

        out[p.get('url').split('.')[0]] = {
            'name': p.get('name'),
            'id': p.get('url').split('.')[0],
            'description': p.get('description'),
            'version': p.get('version'),
            'mc_version': p.get('mcVersion'),
            'author': p.get('author'),
            'logo': p.get('logo'),
            'image': p.get('image'),
            'url': p.get('url'),
            'server_url': p.get('serverPack'),
            'all_versions': old_str,
            'mods': mods_str
        }

    return out