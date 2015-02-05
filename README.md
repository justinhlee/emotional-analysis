# Emotional Analysis of Personal Narrative

Emotion analysis using a series of classifiers on a large data set of personal blog entries.
This project is in progress, and the README will post high-level progress updates.

##Annotating the Data##

###The parser###

I'm working with a subset of the 2009 Spinn3r data set of weblogs[1] that was processed in a previous study to sort out the personal entries from the public news-related ones. I was given a metadata text file that indicated which sections of the XML files contained personal blog entries.

I'm currently just pulling out the content within the description tags of the XML file to simplify the parsing process.
Next step is to tokenize the words. A lot of HTML is muddled with the content that has to be cleaned up.

Some early observations: There are category tags for a large number of blog entries which can be potentially used in the future for features that take advantage of context information. There's also a lot of alternative spellings and a variety of letter cases that also provide additional clues. 

[1] K. Burton, A. Java, and I. Soboroff. The ICWSM 2009 Spinn3r Dataset. In Proceedings of the Third Annual Conference on Weblogs and Social Media (ICWSM 2009), San Jose, CA, May 2009.