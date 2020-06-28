# teilenummer_matcher

## Project idea:
There is a need to find out which parts differ between different model variants in order to be able to plan conversions and clarify them with the audit organisations (e.g. TÜV in Germany). For example you will find which engine parts are different between the 2.5i (N52) and 2.5is (N52) versions of E85.
Therefore my idea to write a small data project that compares the part numbers between two selected models and selected assemblies and outputs the different parts to me in a structured way. 

## Setup:
The whole script will be written in python 3 with some libraries like pandas, flask, etc.

## Workflow
1. The ETK must be structured as CSV or similar
1. I select model, variant and parts group (and subgroup)
1. The script draws me a comparison between the two files and gives me a table that contains all parts that are in table B (e.g. E85 3.0si) but not in table A (e.g. E85 2.5i).  
1. The structure of the table is easy to understand and should contain all important information.

I chose the distinction between category and subcategory because I often need several categories (e.g. front brake disc and rear brake disc) and so I can search on a higher level (e.g. brakes). 

## Next Steps
The next step is to move the whole thing to a small web application (Flask) so that I can use it via browser. Probably I'll build a small interface with Bootstrap 3, my idea is to have a model - engine - year drop down and then based on that also the multi selection of available categories and subcategories. If I click on "Go", I get the table and can export it to CSV or print it (whoever still does that today). 

##Limitations
* The ETK is freely available, but a download is something else. A database is copyrighted and therefore it is not allowed to download it, even if I would only save it in RAM, that would be prohibited. So I can't provide the ETK as a CSV, because the thing is copyrighted, even if it is freely available.
* To run the web application from your own computer, you would need to have Python (and Flask) installed on your system, which is not the case with most Windows users. Due to the ETK problem mentioned above, I can't put the application on a server with a database
* In principle, the comparison is only based upon part numbers. So you still have to think for yourself if it makes sense or if the part number has changed between FL and VFL. 
* You only get the new part numbers. I could think about outputting the old part numbers (which are not included in the new car dataframe) in a separate file/section/column. A direct comparison e.g. based on the name to put the differences directly next to each other is hardly possible. For this purpose, the name in the ETK is not uniform, e.g. "brake disc" vs. "brake disc internally ventilated". This would require a bit of language processing to filter out generic terms and then compare them with keywords. This is not in the scope at the moment
