# ngrokapi
python ngrokapi/app.py 8888

# ngrok
./ngrok http -subdomain=fraser -region eu 8888

# bitbucket
git push -u origin master

# reset heroku project
git remote rm heroku
heroku git:remote -a appname

(
	secret-messenger, test-bot
)

webhook: kjhvvjhkvkgCGHgCJHjghcY6i7Cc7tt

--

User IDs

1266752423417019
1369361663126743
1292335680847606
1252392091503295
1234914753282628
1201944436549689
1391938294211935
1454174931291559
1101743989948322
1124061834357984
1417229798308486
1399267706750548


--

2017-03-19T15:49:52.901360+00:00 app[web.1]: 0.01 (1): SELECT last_time from users where id=1399267706750548
2017-03-19T15:49:52.911254+00:00 app[web.1]: 0.01 (2): SELECT * FROM users WHERE id=1399267706750548
2017-03-19T15:49:52.917418+00:00 app[web.1]: 0.0 (3): DELETE FROM users WHERE id=1399267706750548
2017-03-19T15:49:52.925002+00:00 app[web.1]: ERR: INSERT INTO users (id) VALUES ('1399267706750548'); SELECT currval('users_id_seq')
2017-03-19T15:49:52.927361+00:00 app[web.1]: Traceback (most recent call last):
2017-03-19T15:49:52.927363+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/application.py", line 239, in process
2017-03-19T15:49:52.927365+00:00 app[web.1]:     return self.handle()
2017-03-19T15:49:52.927366+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/application.py", line 230, in handle
2017-03-19T15:49:52.927366+00:00 app[web.1]:     return self._delegate(fn, self.fvars, args)
2017-03-19T15:49:52.927367+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/application.py", line 420, in _delegate
2017-03-19T15:49:52.927368+00:00 app[web.1]:     return handle_class(cls)
2017-03-19T15:49:52.927368+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/application.py", line 396, in handle_class
2017-03-19T15:49:52.927369+00:00 app[web.1]:     return tocall(*args)
2017-03-19T15:49:52.927369+00:00 app[web.1]:   File "/app/app.py", line 19, in POST
2017-03-19T15:49:52.927370+00:00 app[web.1]:     r = bot.recieve(web.data(), session)
2017-03-19T15:49:52.927371+00:00 app[web.1]:   File "/app/bot/recieve.py", line 16, in recieve
2017-03-19T15:49:52.927371+00:00 app[web.1]:     v = recieveVal(info, sess)
2017-03-19T15:49:52.927372+00:00 app[web.1]:   File "/app/bot/recieve.py", line 51, in recieveVal
2017-03-19T15:49:52.927373+00:00 app[web.1]:     return new_user(sess,id)
2017-03-19T15:49:52.927373+00:00 app[web.1]:   File "/app/bot/recieve.py", line 88, in new_user
2017-03-19T15:49:52.927374+00:00 app[web.1]:     db.insert('users',id=sess.id)
2017-03-19T15:49:52.927375+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/db.py", line 777, in insert
2017-03-19T15:49:52.927376+00:00 app[web.1]:     self._db_execute(db_cursor, sql_query)
2017-03-19T15:49:52.927376+00:00 app[web.1]:   File "/app/.heroku/python/lib/python2.7/site-packages/web/db.py", line 587, in _db_execute
2017-03-19T15:49:52.927377+00:00 app[web.1]:     out = cur.execute(query, params)
2017-03-19T15:49:52.927377+00:00 app[web.1]: OperationalError: currval of sequence "users_id_seq" is not yet defined in this session
