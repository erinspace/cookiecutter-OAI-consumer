cookiecutter-OAI-consumer
=========================

You can use this cookiecutter template to create a very basic consumer for the SHARE project,if the API you're writing for uses the OAI-DC metadata format. 

Here's how to create your own OAI consumer: 
 ... coming soon ...

1.  Install the cookiecutter python library

Here's a link to the [cookiecutter github repo](https://github.com/audreyr/cookiecutter) and a link to the [installation instructions](http://cookiecutter.readthedocs.org/en/latest/installation.html) in the cookiecutter documentation.  

Consider using a new [virtual enviornment](http://virtualenv.readthedocs.org/en/latest/virtualenv.html), and running  
    `pip install cookiecutter` 

2. In a terminal, from the directory you'd like to create your consumer folder, type:
  ` cookiecutter https://github.com/erinspace/cookiecutter-OAI-consumer.git`

3. You'll clone the base git repo and begin the cookie cutting process! 

  * repoNmae: enter what you'd like the repo to be called.
  * oaiDcBase: the base url for the OAI-PMH API call, all the way up to (and including) the question mark. Some examples:
    - http://digitalcommons.wayne.edu/do/oai/?
    - http://ideals.uiuc.edu/dspace-oai/request?
    - http://opensiuc.lib.siu.edu/do/oai/?
  * dateGranularity: Check out the date granularity that your particular API preferes, by visiting the base url and then appending verb=Identify.  Some examples of dateGranularity: 
    - YYYY-MM-DDThh:mm:ssZ
    - YYYY-MM-DD hh:mm:ss
    - YYYY-MM-DD
  * metadataPrefix: In most cases, this will be the base value of "oai_dc," but we wanted to make it flexible enough to request different prefixes if the API you're using has them! 
  * hasRestrictedSets: True or False. If your OAI API has sets you'd rather not put into your SHARE consumer, set this value to True. Then, make sure to include a text file with the names of all of the sets you __would__ like to include.
  * approvedSeriesNamesFilename: only relevant if you've set the above to True. This file should have the sets to be included, one on each line. Here's a (short example) of a text file: 
    `ad_pubs
    agecon_articles
    agecon_wp
    anat_pubs
    anthro_pubs
    arch_videos
    asfn_articles
    auto_pres
    ccj_articles
    cee_pubs
    chem_mdata
    chem_pubs
    cs_pubs
    cs_sp `
