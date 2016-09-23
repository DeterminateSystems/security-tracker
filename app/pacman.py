from config import basedir
from pycman.config import init_with_config
from pyalpm import vercmp
from app.util import cmp_to_key
from operator import attrgetter
from os import chdir

archs = ['i686', 'x86_64']
repos = {'i686': ['core', 'extra', 'community', 'testing', 'community-testing'],
         'x86_64': ['core', 'extra', 'community', 'multilib', 'testing', 'community-testing', 'multilib-testing']}
configpath = './pacman/arch/{}/pacman.conf'
chdir(basedir)


def get_handle(arch):
    return init_with_config(configpath.format(arch))


def update(arch=None, force=False):
    update_archs = [arch] if arch else archs
    for arch in update_archs:
        for syncdb in get_handle(arch).get_syncdbs():
            syncdb.update(force)


def get_pkg(pkgname, arch=None, testing=True, filter_arch=False):
    get_archs = [arch] if arch else archs
    results = set()
    for arch in get_archs:
        for syncdb in get_handle(arch).get_syncdbs():
            if not testing and 'testing' in syncdb.name:
                continue
            result = syncdb.get_pkg(pkgname)
            if result:
                results.add(result)
    results = sort_packages(results)
    results = filter_duplicates(results, filter_arch)
    return results


def search(pkgname, arch=None, testing=True, filter_arch=False):
    search_archs = [arch] if arch else archs
    results = []
    for arch in search_archs:
        for syncdb in get_handle(arch).get_syncdbs():
            if not testing and 'testing' in syncdb.name:
                continue
            result = syncdb.search(pkgname)
            if result:
                results.append(result)
    results = sort_packages(results)
    results = filter_duplicates(results, filter_arch)
    return results


def filter_duplicates(packages, filter_arch=False):
    filtered = []
    for pkg in packages:
        contains = False
        for f in filtered:
            if f.version != pkg.version or f.db.name != pkg.db.name:
                continue
            if not filter_arch and f.arch != pkg.arch:
                continue
            contains = True
            break
        if not contains:
            filtered.append(pkg)
    return filtered


def sort_packages(packages):
    packages = sorted(packages, key=lambda item: item.arch)
    packages = sorted(packages, key=lambda item: item.db.name)
    packages = sorted(packages, key=cmp_to_key(vercmp, attrgetter('version')), reverse=True)
    return packages
