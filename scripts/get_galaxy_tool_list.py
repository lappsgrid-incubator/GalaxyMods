#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program is to:

"""
import sys

import re

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'krim'
__date__ = '5/24/17'
__email__ = 'krim@brandeis.edu'

from bs4 import BeautifulSoup
import json


tool_conf_file = open("../config/tool_conf.xml")
conf_soup = BeautifulSoup(tool_conf_file, 'lxml')

tools = set()

for tool_def in conf_soup.find_all("tool"):
    tools.add(tool_def["file"])

tool_conf_file.close()

license_clauses = json.load(open("clauses.json"))
for tool in tools:
    print tool
    tool_group, tool_name = re.sub(r"\.xml$", "", tool).split("/")
    print tool_group, tool_name
    if license_clauses.has_key(tool_group):
        tool_xml_file = open("../tools/{}".format(tool))
        tool_soup = BeautifulSoup(tool_xml_file)
        help_tag = tool_soup.find("help")
        new_help = "\nLicense\n-------\n\n" + \
                   license_clauses[tool_group]
        if help_tag is not None:
            if "Licence\n" in ' '.join([str(e) for e in help_tag.contents]):
                new_help = ""
        else:
            help_tag = tool_soup.new_tag("help")
            tool_soup.tool.append(help_tag)
        help_tag.append(new_help)
        tool_soup.tool.insert
        print tool_soup.tool
        tool_xml_file.close()

        with open("../tools/{}".format(tool), "w") as out_file:
            out_file.write(str(tool_soup.tool.prettify()))


# print tools



