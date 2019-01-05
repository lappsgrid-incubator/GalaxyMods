
import ac.uk.lancs.ucrel.semtaggers.web.clients.SemanticTaggerClient;
import groovy.json.*
import static org.lappsgrid.discriminator.Discriminators.*
import org.lappsgrid.serialization.*
import org.lappsgrid.serialization.lif.*

WAITING = 0
PROCESSING = 1

File input = new File(args[0])
File output = new File(args[1])

DataContainer data = Serializer.parse(input.text, DataContainer)

//def text = "A 33 year-old man with past medical history significant for dizziness/fainting spells received the following vaccines on 10 March 2010: VAX1 (lot number not reported); and VAX2 (lot number not reported either). Ten days after vaccination, he developed shortness of breath and chest pain and was subsequently diagnosed with myocarditis. On Day 20 (30 March 2010) post vaccination, the following tests were performed: an electrocardiogram which was reported to be normal and troponin I levels were measured and found to be 12.3 ng/ml (abnormal). Patient died on 02 April 2010. COD: heart failure. List of documents held by sender: None."
def tagger = new SemanticTaggerClient()

def text = data.payload.text
String tagged = tagger.tagEngText(text)
println tagged

if (data.payload instanceof Map) {
    data.payload = new Container(data.payload)
}
//println data.asPrettyJson()
data.payload = process(data.payload, tagged)
String json = data.asPrettyJson()
//println json
output.text = json
return

Container process(Container container, String input) {
    View view = container.newView()
    view.addContains(Uri.SEMANTIC_ROLE, this.class.name, "semantic role")
    int state = WAITING
    int count = 0
    input.eachLine { String line ->
        if (state == WAITING) {
            if (line.startsWith('S_BEGIN')) {
                state = PROCESSING
            }
        }
        else if (state == PROCESSING) {
            if (line.startsWith('S_END')) {
                state = WAITING
            }
            else {
                Annotation a = view.newAnnotation()
                a.atType = Uri.SEMANTIC_ROLE
                a.id = "SR-${++count}"
                String[] parts = line.split('\t')
                a.features['word'] = parts[0]
                a.features['lemma'] = parts[1]
                a.features['pos'] = parts[2]
                a.features['semtag'] = parts[3]
                a.features['mwe'] = parts[4]
                a.features['tags'] = makeTags(parts[5])
            }
        }
    }
    return container
}

List makeTags(String input) {
    return input.tokenize(';').collect { makeTag(it.trim()) }
}

Map makeTag(String input) {

    int space = input.indexOf(' ')
    Map map = [:]
    if (space > 0) {
        map.tag = input.substring(0, space)
        map.labels = input.substring(space + 1)[1..-2].tokenize(',').collect { it.trim() }
    }
    return map
}


