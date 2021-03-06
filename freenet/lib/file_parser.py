#!/usr/bin/env python3
"""文件解析器,对dns分发的rules和白名单ip列表进行解析
文件格式:一条规则就是一行,#开头的表示注解:
"""


class FilefmtErr(Exception): pass


def __drop_comment(line):
    """删除注释"""
    pos = line.find("#")
    if pos < 0:
        return line
    return line[0:pos]


def __read_from_file(fpath):
    result = []
    fdst = open(fpath, "rb")

    for line in fdst:
        line = line.decode("iso-8859-1")
        line = __drop_comment(line)
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        line = line.lstrip()
        line = line.rstrip()
        if not line: continue
        result.append(line)
    fdst.close()

    return result


def parse_host_file(fpath):
    """解析主机文件,即域名规则文件"""
    lines = __read_from_file(fpath)
    results = []
    for line in lines:
        find = line.find(":")
        if find < 1: continue
        a = line[0:find]
        e = find + 1
        try:
            b = int(line[e:])
        except ValueError:
            continue
        results.append((a, b,))
    return results

def __get_ip_subnet(line):
    """检查子网格式是否正确"""
    pos = line.find("/")
    if pos < 7: return None
    ipaddr = line[0:pos]
    pos += 1

    try:
        mask = int(line[pos:])
    except:
        return None

    return (ipaddr, mask,)


def parse_ip_subnet_file(fpath):
    """解析IP地址列表文件"""
    lines = __read_from_file(fpath)
    results = []
    for line in lines:
        ret = __get_ip_subnet(line)
        if not ret: print("the wrong format on: %s" % line)
        results.append(ret)

    return results


def get_linux_host_nameservers(resolv_path="/etc/resolv.conf"):
    """获取LINUX系统的所有nameservers
    :param resolv_path: nameserver的配置文件
    """
    fdst = open(resolv_path, "r")
    nameservers = []

    for line in fdst:
        ts = line.lstrip()
        if ts[0] == "#": continue
        if ts[0:10] != "nameserver": continue
        replaces = ("\r", "\n", "nameserver")
        for s in replaces: ts = ts.replace(s, "")
        ts = ts.lstrip()
        ts = ts.rstrip()
        nameservers.append(ts)

    return nameservers