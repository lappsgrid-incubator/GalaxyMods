import commands, sys, os, json, subprocess
from nlp_brat import nlp

def run(json_string):
    reload(sys);
    sys.setdefaultencoding('utf8')
    #lappsjsonfil = hda.dataset.file_name

    data = nlp.brat(json_string)
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    with open('/Users/suderman/Workspaces/IntelliJ/Services/brat/src/test/resources/stanford-dep.lif') as json_file:
        run(json_file.read())
    print("Done.")
