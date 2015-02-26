![](https://cldup.com/7hlmNJ5hVP-2000x2000.png)


Table of Contents
-----------------
1. [Overview]()
2. [Data sources]()
3. [Tools used]()
4. [Lessons learned]()
5. [Contributing]()


Overview
--------

Seattle (the repo) aims to make it easy to understand what sort of changes are happening in your neighborhood. Change seems to be acclerating in Seattle; we want to find out if those changes have had a measureable impact on the type and frequency of 911 Emergency responses within the city limits.

We are aware that Socrata provides a similar (and more robust) [service](http://web6.seattle.gov/mnm/incidentresponse.aspx), but it requires some effort to parse and doesn't immediately provide answers to the questions we intend to answer.

Credit goes to [Joel 'Grandpa' Stanner](https://github.com/poolbath1) for the idea.


Data sources
------------

1. [Seattle Fire Real-Time 911](http://www2.seattle.gov/fire/realtime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des)
2. [data.seattle.gov](https://data.seattle.gov/)
3. [Zillow Neighborhood data](https://www.zillow.com/howto/api/neighborhood-boundaries.htm)


Tools used
----------

Seattle was written using the following:
- Amazon EC2
- Amazon RDS
- Mapbox
- Postgresql/PostGIS
- Postico
- Pyramid


Lessons learned
---------------

1. Don't geocode.
2. Embrace the merge conflict.
3. Somehow pair programming seems to work.
4. Naps are under-rated.
5. I should not be in charge of writing README's.


Contributing
------------

We worked on this for a week. There are no hard and fast rules about what you can or can't do. Becoming a contributor is as easy as opening a Pull Request :wink:

__Feedback is welcome and encouraged.__ What did we do right? Wrong? Inefficiently? [Open a ticket](https://github.com/jacquestardie/seattle/issues), give us some advice, and Constantine will send you cupcakes. Promise.

Thanks!
[:older_man:](https://github.com/poolbath1) [:hurtrealbad:](https://github.com/constanthatz) [:bowtie:](https://github.com/bm5w) [:cat:](https://github.com/jqtrde)


