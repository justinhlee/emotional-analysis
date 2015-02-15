# Emotional Analysis of Personal Narrative

Emotion analysis using a series of classifiers on a large data set of personal blog entries.
This project is in progress, and the README will post high-level progress updates.

##Annotating the Data##



###Preprocess the Given Data###

I'm working with a subset of the 2009 Spinn3r data set of weblogs[1] that was processed in a previous study to sort out the personal entries from the public news-related ones. I was given a metadata text file that indicated which sections of the XML files contained personal blog entries, so the first part of annotating the data requires me to pull out the relevant sections which we will run through CoreNLP[2]. 


###Run CoreNLP on the Personal Entries###
The output files from the previous step are to be run through Stanford's CoreNLP tool, mainly for tokenization and lemmatisation. 

```
java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,cleanxml,ssplit,pos,lemma -filelist entries.txt -outputDirectory entries-output

```

###Tag the CoreNLP XML Output Files###







[1] K. Burton, A. Java, and I. Soboroff. The ICWSM 2009 Spinn3r Dataset. In Proceedings of the Third Annual Conference on Weblogs and Social Media (ICWSM 2009), San Jose, CA, May 2009.

[2] Manning, Christopher D., Surdeanu, Mihai, Bauer, John, Finkel, Jenny, Bethard, Steven J., and McClosky, David. 2014. The Stanford CoreNLP Natural Language Processing Toolkit. In Proceedings of 52nd Annual Meeting of the Association for Computational Linguistics: System Demonstrations, pp. 55-60.

