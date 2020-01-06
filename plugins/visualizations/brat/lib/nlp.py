import os, json
from brat_types import entity_types

class Uri:
    BASE = "http://vocab.lappsgrid.org"
    TOKEN = BASE + "/Token"
    POS = BASE + "/Token#pos"
    LEMMA = BASE + "/Token#lemma"
    NE = BASE + "/NamedEntity"
    PHRASE_STRUCTURE = BASE + "/PhraseStructure"
    CONSTITUENT = BASE + "/Constituent"
    DEPENDENCY_STRUCTURE = BASE + "/DependencyStructure"
    DEPENDENCY = BASE + "/Dependency"
    MARKABLE = BASE + "/Markable"
    RELATION = BASE + "/GenericRelation"

class ColorPicker:
    colors = [ "#7fa2ff", "#8fb2ff", "#95dfff", "#a4bced", "#adf6a2", "#ccadf6", "#ccdaf6", "#e3e3e3", "#e4cbf6", "#f1f447", "#ffccaa", "#ffe000", "#ffe8be", "#fffda8", "lightblue", "lightgray", "lightgreen" ]

    def __init__(self):
        self.index = 0

    def next(self):
        if self.index >= len(ColorPicker.colors):
            self.index = 0
        color = ColorPicker.colors[self.index]
        self.index = self.index + 1
        return color

color_picker = ColorPicker()

relation_types = [ {
    "args" : [ {
        "role" : "Arg1",
        "targets" : [ "Mention" ]
    }, {
        "role" : "Arg2",
        "targets" : [ "Mention" ]
    } ],
    "arrowHead" : "none",
    "name" : "Coref",
    "labels" : [ "Coreference", "Coref" ],
    "children" : [ ],
    "unused" : False,
    "dashArray" : "3,3",
    "attributes" : [ ],
    "type" : "Coreference",
    "properties" : {
        "symmetric" : True,
        "transitive" : True
    }
} ]


relation_types_index = dict()
relation_types_index['Coreference'] = relation_types[0]

log = list()

def load_entity_types():
    base_path = os.getcwd() + '../mods/plugins/visualizations/brat/lib/brat_types.py'
    with open(base_path) as src:
        return json.load(src)

# def next_color():
#     if color_index >= len(colors):
#         color_index = 0
#     color = colors[color_index]
#     color_index = color_index + 1
#     return color

def register_dependency_type(type_name):
    if type_name in relation_types_index:
        return

    type = {
        'type': type_name,
        'labels': [ type_name ],
        'bgColor': color_picker.next(),
        'args': [
            {'role': 'Governor', 'targets':['Entity']},
            {'role': 'Dependent', 'targets':['Entity']}
        ]
    }
    relation_types.append(type)
    relation_types_index[type_name] = type

def register_structure_type(type_name):
    if type_name in relation_types_index:
        return
    type = {
        'type': type_name,
        'labels': [ type_name ],
        'bgColor': color_picker.next(),
        'args': [
            {'role': 'Parent', 'targets':['Relation']},
            {'role': 'Child', 'targets':['Relation', 'Entity']}
        ]
    }
    relation_types.append(type)
    relation_types_index[type_name] = type

def createEntity(annotation):
    entity = list()
    entity.append(annotation['id'])
    entity.append(getLabel(annotation))
    offsets = [[ annotation['start'], annotation['end'] ]]
    entity.append(offsets)
    return entity

# def createRelation(annotation):
#     type = annotation['@type']
#     if type == Uri.DEPENDENCY:
#         return createDependency(annotation)
#     if type == Uri.CONSTITUENT:
#         return createPhraseStructure(annotation)
#     return None
#
# def createPhraseStructure(relations, annotation):
#     label = annotation['label']
#     if 'ROOT' == label:
#         root = [
#             annotation['id'],
#             label,
#             [[]]
#         ]
#         return
#
#     features = annotation['features']
#     register_structure_type(label)
#     parent = features['parent']
#     for child in features['children']:
#         node = list()
#         node.append()

def processPhraseStructure(annotations):
    relations = list()
    root = {
        'type': 'ROOT',
        'labels': [ 'ROOT'],
        'bgColor': color_picker.next(),
        'args': [
            {'role': 'Child', 'targets': ['Relation', 'Entity']},
            {'role': 'Parent', 'targets': ['Relation'] }
        ]
    }
    relation_types.append(root)
    relation_types_index['ROOT'] = root
    for a in annotations:
        if a['@type'] == Uri.CONSTITUENT:
            features = a['features']
            label = a['label']
            relation = list()
            relation.append(a['id'])
            relation.append(label)
            args = list()
            if label == 'ROOT':
                args.append(['Parent', a['id']])
            else:
                args.append(['Parent', features['parent']])
            # for child in features['children']:
            #     args.append(['Child', child])
            child = features['children'][0]
            args.append(child)
            relation.append(args)
            relations.append(relation)
    return relations

def createDependency(annotation):
    features = annotation['features']
    if 'governor_word' not in features:
        return None

    type = annotation['label']
    register_dependency_type(type)
    relation = list()
    relation.append(annotation['id'])
    relation.append(type)
    relation.append([ ['Governor', features['governor']], [ 'Dependent', features['dependent']] ])
    return relation


def getLabel(annotation):
    type = annotation['@type']
    if type == Uri.NE:
        return annotation['features']['category']
    if is_token(type):
        return annotation['features']['pos']
    if type == Uri.MARKABLE:
        if annotation['label'] != None:
            return annotation['label']
        return 'Markable'
    if type == 'Tagger' and 'type' in annotation['features']:
        return annotation['features']['type']
    if annotation['label'] != None:
        return annotation['label']
    return 'Entity'

def processDependencies(annotations):
    # names = list()
    relations = list()
    for a in annotations:
        if a['@type'] == Uri.DEPENDENCY:
            # label = getLabel(a)
            # if label not in names:
            #     names.append(label)
            relation = createDependency(a)
            if relation is not None:
                relations.append(relation)
    return relations

def make_args(arr):
    if type(arr) == str:
        arr = arr[1:-1].split(",")
    return [ ['Parent', arr[0]], ['Child', arr[1]]]


def processGenericRelations(annotations):
    relations = list()
    for a in annotations:
        if a['@type'] == Uri.RELATION:
            if 'label' in a['features']:
                type = a['features']['label']
            else:
                type = 'Rel'
            #type = a['features']['label']
            register_structure_type(type)
            relation = [
                a['id'],
                type,
            ]
            relation.append(make_args(a['features']['arguments']))
            relations.append(relation)
    return relations

def is_token(type):
    return type in [Uri.TOKEN, Uri.POS, 'Token', 'Token#pos']

def is_viewable(a):
    type = a['@type']
    return is_token(type) or type in [ Uri.NE, Uri.MARKABLE, 'Tagger' ]

def brat(lappsJson):
    docData = {}
    data = json.loads(lappsJson)
    container = data['payload']
    view = container['views'][-1]
    annotations = view['annotations']
    docData['text'] = container['text']['@value']
    # object['entities'] = [ createEntity(a, list) for a in annotations ]
    entities = [createEntity(a) for a in annotations if is_viewable(a)]
    # ne = [ createEntity(a) for a in annotations if a['@type'] == Uri.NE ]
    # markables = [ createEntity(a) for a in annotations if a['@type'] == Uri.MARKABLE ]
    docData['entities'] = entities

    dependency_parse = processDependencies(annotations)
    constituency_parse = processPhraseStructure(annotations)
    relations = processGenericRelations(annotations)

    docData['relations'] = dependency_parse + constituency_parse + relations

    collData = dict()
    collData['entity_types'] = entity_types
    collData['relation_types'] = relation_types
    
    return {
        'annotations': json.dumps(docData),
        'config': json.dumps(collData),
    }

if __name__ == '__main__':
    # with open('/Users/suderman/Workspaces/IntelliJ/Services/brat/src/test/resources/stanford-dep.lif') as json_file:
    #     brat_data = brat(json_file.read())
    with open('/Users/suderman/Desktop/tokens_pos.lif') as json_file:
        brat_data = brat(json_file.read())

    print json.dumps(brat_data, indent=4)
