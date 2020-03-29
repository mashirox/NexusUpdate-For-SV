from requests import get
from os import getcwd, listdir
from os.path import join, isfile
from re import compile, findall, S
from pyquery import PyQuery as pq

mod_version = []
mod_name = []
nexus_id = []
id_pattern = compile('"Version": "(.*?)"', S)
name_pattern = compile('"Name": "(.*?)"', S)
nexus_pattern = compile('"Nexus:(.*?)"', S)

base_url = "https://www.nexusmods.com/stardewvalley/mods/{}?tab=files"


def compare_version(version1: str, version2: str) -> int:  # mark return
    v1, v2 = ([*map(int, v.split('.'))] for v in (version1, version2))
    d = len(v2) - len(v1)
    v1, v2 = v1 + [0] * d, v2 + [0] * -d
    return (v1 > v2) - (v1 < v2)


def get_mod_version():
    root_dir = getcwd()
    ls = listdir(root_dir)
    for i in ls:
        if not isfile(i):
            file_path = join(i, "manifest.json")
            try:
                with open(file_path, "r") as f:
                    mod_info = f.read()
                    version = findall(id_pattern, mod_info)
                    name = findall(name_pattern, mod_info)
                    nexus = findall(nexus_pattern, mod_info)
                    mod_version.append(version)
                    mod_name.append(name)
                    nexus_id.append(nexus)
            except FileNotFoundError as e:
                print("请检查是否把检查程序放入Mods文件夹")


def check_update():
    cnt = 0  # Need Update Mod
    for i in range(len(nexus_id)):
        if len(nexus_id[i]) != 0:  # Check Array isn't Empty
            data = get(base_url.format(nexus_id[i][0])).text
            doc = pq(data)
            new_info = doc("#file-container-main-files dt .stat-version .stat").items()
            for each in new_info:
                now_version = each.text()
                if compare_version(now_version, mod_version[i][0]) == 1:
                    print(mod_name[i][0] + "需要更新 !    " + "当前版本：" + str(mod_version[i][0]) + "    最新版本：" + str(
                        now_version))
                    cnt += 1
                break

    if cnt == 0:
        print("你当前的Mod已经是最新!")


if __name__ == '__main__':
    print("本程序开源，By：")
    get_mod_version()
    check_update()
