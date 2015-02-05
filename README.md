# Emotional Analysis of Personal Narrative

Emotion analysis using a series of classifiers on a large data set of personal blog entries.
This project is in progress, and the README will post high-level progress updates.

##Annotating the Data##

###The parser###

The xml file doesn't have additional namespaces so currently just pulling out the content within the description tags.
Next step is to tokenize the words. A lot of HTML is muddled with the content that has to be cleaned up.

There are category tags for a large number of blog entries which can be potentially used in the future for features that take advantage of context information.