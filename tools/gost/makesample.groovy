
String name = 'sample2.lif'
Container container = new Container()
container.text = 'A 33 year-old man with past medical history significant for dizziness/fainting spells received the following vaccines on 10 March 2010: VAX1 (lot number not reported); and VAX2 (lot number not reported either). Ten days after vaccination, he developed shortness of breath and chest pain and was subsequently diagnosed with myocarditis. On Day 20 (30 March 2010) post vaccination, the following tests were performed: an electrocardiogram which was reported to be normal and troponin I levels were measured and found to be 12.3 ng/ml (abnormal). Patient died on 02 April 2010. COD: heart failure. List of documents held by sender: None.'
container.language = 'en'
Data data = new Data(Uri.LIF, container)
/*
Map data = [ 
	discriminator: Uri.LIF,
	payload: container
]
*/
new File(name).text = data.asPrettyJson()

