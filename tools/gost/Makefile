-include env.mk

groovy:
	if [ src/semtagger.groovy -nt semtagger.groovy ] ; then cp src/semtagger.groovy . ; fi
	groovyc -cp $(LIBS) semtagger.groovy
	
env: 
	./makeenv.sh > env.sh

env.mk: env.sh
	cat $< | sed 's/"//g ; s/=/:=/g' > $@

test:
	echo $(LIBS)
	java -cp .:$(LIBS) semtagger sample2.lif sample2-gost.lif

clean:
	rm *.class
	rm semtagger.groovy

	

	