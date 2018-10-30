# "Database code" for the DB Forum.
#!/usr/bin/python
# -*- coding: utf-8 -*-
#Written in python version 3.7.0
import psycopg2
newsDB = "news"

# QUESTION NUMBER 1 !!!!!!!!!!!!!!!!!!!!!!!!!!
# find 3 most popular articles like so with most popular at top (desc order):
# "Article title" - 100 views

def top_three_posts():
  """Authors ranked by most page views on their articles."""
  db = psycopg2.connect(database=newsDB)
  c1 = db.cursor()
# ------------------------------
  c1.execute(
  """
  CREATE VIEW popularity_chart AS
      SELECT SPLIT_PART(path::text, '/', 3) AS slug,
      COUNT(*) AS view_count
      FROM log
      GROUP BY path ORDER BY view_count DESC offset 1 limit 8;
  Select articles.title, popularity_chart.view_count
  FROM articles JOIN popularity_chart
  ON articles.slug = popularity_chart.slug
  ORDER BY popularity_chart.view_count DESC
  Limit 3;
  """
  )
# ------------------------------
  statement1 = c1.fetchall()
  print("Article popularity by total views (Top 3):")
  for row in statement1:
    print('   \"' + row[0].title() + '\"' + ' - ' + str(row[1]) + ' views')
  db.close()
# --------------------

# QUESTION NUMBER 2 !!!!!!!!!!!!!!!!!!!!
# Which authors got the most page views?
# count the views of each article
# sum up all the views belonging to each writer
# output all authors as follows in desc order:
# author name - 100 views

def popular_authors():
  """Authors ranked by most page views on their articles."""
  db = psycopg2.connect(database=newsDB)
  c2 = db.cursor()
# ------------------------------
  c2.execute(
    """
    SELECT name, COUNT(*) AS all_art_count
    FROM authors, articles, log
    WHERE authors.id = articles.author AND log.path like '%' || articles.slug
    GROUP BY name
    ORDER BY all_art_count DESC;
    """
    )

  statement2 = c2.fetchall()
  print('---///---///---///---')
  print("Author popularity by article views (all authors) :")
  for row in statement2:
      print("   " + row[0].title() + ' - ' + str(row[1]) + ' views')
  db.close()

# QUESTION 3 !!!!!!!!!!!!!!!!!!!!!!!!!!
# Print out the days and % of errors for every day that had more than 1%
# of requests returning errors:
# Month day, year - 10% errors

def error_days():
  """find days where more than 1% of requests led to errors"""
  db = psycopg2.connect(database=newsDB)
  c3 = db.cursor()
  # ------------------------------
  c3.execute(
  """
  CREATE VIEW log_status_getter AS
      SELECT count(*) AS failures,
      status, log.time::timestamp::date AS readable_date
      FROM log WHERE status LIKE '%404%'
      GROUP BY status, readable_date
      ORDER BY failures desc;
  CREATE VIEW all_hits AS
      SELECT count(*) AS raw_hits,
      log.time::timestamp::date AS time_of_visit
      FROM log
      GROUP BY time_of_visit;
  CREATE VIEW joint_visit_status AS
      SELECT * FROM log_status_getter
      JOIN all_hits
      ON log_status_getter.readable_date = all_hits.time_of_visit;
  CREATE VIEW miss_rate AS
      SELECT round((failures*100.0)/raw_hits, 3) AS
      rate, to_char(time_of_visit, 'Mon DD, YYYY')
      FROM joint_visit_status;
  SELECT * from miss_rate WHERE rate > 1
  ORDER BY rate DESC;
  """
  )
  print('---///---///---///---')
  print("Days with error rate above 1% :")
  statement3 = c3.fetchall()
  for row in statement3:
    print('   On ' + row[1] + " - " + str(row[0]) + '% of requests were errors')
  db.close()

  # ------------------------------
print("Running Log Analysis, Please be patient while we calculate your queries")
print('---///---///---///---')
top_three_posts()
popular_authors()
error_days()
