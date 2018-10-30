<b>Logs Analysis Project:</b>

A project utilizing SQL to practice making views and queries to fetch information from a database.

<b>General Project Overview:</b>

The objective of this program was to use a given database that emulated an news-article website and report information about the site regarding the following 3 questions:
	1) What are the top 3 most popular articles by views?
	2) Who are the most-viewed authors on the site?
	3) On which days were more than 1% of website requests resultant in 404 errors?

<b>Requirements:</b>

Python 3 - Coded in version 3.7, but 3.6 version-variants should work too

Virtual Box --
https://www.virtualbox.org/wiki/Downloads

Vagrant --
https://www.vagrantup.com/downloads.html

(Note: This project was made and tested on a Windows machine, but should work on both Mac and Windows systems)

<b>Project setup:</b>

1) In order to get the database for this project, we need to download some files to the virtual machine’s directory.
First, make a clone of the relevant repository at <i>fullstack-nanodegree-vm</i>

(https://github.com/udacity/fullstack-nanodegree-vm)

2) Download the example news-site's data from the following link, unzip it, and put it in the <b>vagrant</b> directory for your Vitrual Machine

(https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

3) Put the ```logdb.py``` file from this project into your <b>vagrant</b> directory.

4) Open up command line, and navigate to your <b>vagrant</b> directory

5) run ```vagrant up``` and ```vagrant ssh ``` to get turn on the virtual machine and log into it.

(```vagrant up``` may take some time to load things up if it's the first time you're running that command on the Virtual Machine)

(Also, running ```vagrant ssh``` is like logging in, and depending on your settings, you might not have to actually give a user-name and password)

6) Navigate to the Virtual Machine’s <b>vagrant</b> directory with
```cd /vagrant``` (as indicated by the command prompt's reminder, which was made by the previously downloaded files)

7) type ```python logdb.py``` to run the code in the Virtual Machine.

<b>Note:</b> All SQL views are created within the python code's execution, so you shouldn't have to change the database before running the code.
However, all views are listed out below for clarity:

```
 CREATE VIEW popularity_chart AS
      SELECT SPLIT_PART(path::text, '/', 3) AS slug,
      COUNT(*) AS view_count
      FROM log
      GROUP BY path ORDER BY view_count DESC offset 1 limit 8;
			```
```
 CREATE VIEW log_status_getter AS
      SELECT count(*) AS failures,
      status, log.time::timestamp::date AS readable_date
      FROM log WHERE status LIKE '%404%'
      GROUP BY status, readable_date
      ORDER BY failures desc;
			```
```
  CREATE VIEW all_hits AS
      SELECT count(*) AS raw_hits,
      log.time::timestamp::date AS time_of_visit
      FROM log
      GROUP BY time_of_visit;
			```

  ```
	CREATE VIEW joint_visit_status AS
      SELECT * FROM log_status_getter
      JOIN all_hits
      ON log_status_getter.readable_date = all_hits.time_of_visit;
			```

  ```
	CREATE VIEW miss_rate AS
      SELECT round((failures*100.0)/raw_hits, 3) AS
      rate, to_char(time_of_visit, 'Mon DD, YYYY')
      FROM joint_visit_status;
			```

<b>Additional Notes:</b>

Special thanks to <i>Gabriel B.</i> for advice in helping to create views.
