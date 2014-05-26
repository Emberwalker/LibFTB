__author__ = 'Arkan'

import argparse
import sys
import textwrap
import time
import urllib.request

import libftb.ftb


download_last_mark = 0


def main():
    __parse_argv(sys.argv)


def __parse_argv(argv):
    root = argparse.ArgumentParser()
    subcmds = root.add_subparsers(help='sub-command help')

    ls = subcmds.add_parser('list', help='List modpacks.')
    ls.set_defaults(func=__list)

    info = subcmds.add_parser('details', help='Get modpack details')
    info.add_argument(action='store', dest='pack')
    info.set_defaults(func=__details)

    fetch = subcmds.add_parser('fetch', help='Fetch a modpack zip.')
    fetch.add_argument('-s', '--server', action='store_true', dest='server')
    fetch.add_argument(action='store', dest='pack')
    fetch.set_defaults(func=__fetch)

    args = root.parse_args(argv[1:])
    try:
        args.func(args)
    except AttributeError:
        root.exit(-1, "Invalid input; run with --help for help.\n")


def __list(args):
    packs = libftb.ftb.get_packs()
    print('Available packs:')
    for _, p in packs.items():
        print("\t{} ({}) {}".format(p['name'], p['id'], p['version']))


def __details(args):
    packs = libftb.ftb.get_packs()
    try:
        p = packs[args.pack]
        print("Details for {} ({}):".format(p['name'], p['id']))
        print("\t    Version: {}".format(p['version']))
        print("\t  Minecraft: {}".format(p['mc_version']))
        print("\t     Author: {}".format(p['author']))

        print()

        desc = textwrap.wrap(p['description'], 100)
        first = True
        for l in desc:
            if first:
                first = False
                print("\tDescription: {}".format(l))
            else:
                print("\t             {}".format(l))

        print()

        count = 1
        mods = ""
        for m in p['mods']:
            if (count % 3) == 0:
                mods += "{},\n".format(m)
            else:
                mods += "{}, ".format(m)
            count += 1
        mods = mods[:len(mods) - 2]

        first = True
        for l in mods.splitlines():
            if first:
                first = False
                print("\t       Mods: {}".format(l))
            else:
                print("\t             {}".format(l))

    except KeyError:
        print("No pack found for name {}".format(args.pack))


def __fetch(args):
    packs = libftb.ftb.get_packs()
    try:
        p = packs[args.pack]
        server = args.server

        if server:
            url = libftb.ftb.get_pack_url(p, server=server)
            fname = p['server_url']
        else:
            url = libftb.ftb.get_pack_url(p)
            fname = p['url']

        try:
            print("Downloading {}...".format(url), end='')
            start = time.time()
            urllib.request.urlretrieve(url, fname, reporthook=__download_print_dots)
            end = time.time()
            print(" Done in {:.2f} seconds.".format(end - start))
            print("Saved archive as {}".format(fname))
        except Exception as ex:
            print(" Failed to download pack: {}".format(ex))
    except KeyError:
        print(" No pack found for name {}".format(args.pack))


def __download_print_dots(block, block_size, total_bytes):
    import ftb
    per = float(block*block_size) / total_bytes
    per = round(per*100, 2)
    if (per % 5) == 0 and per > ftb.download_last_mark:
        ftb.download_last_mark = per
        print('.', end='', flush=True)


if __name__ == "__main__":
    main()