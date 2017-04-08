# Fake Open Graph Server
'fake-og-server' is a Fake Open Graph server written in python3.
This app receives 'Source Url' and 'Target Url', displays the Open Graph information of 'Source Url' and redirects it to 'Target Url'.

# Configuration

edit `config.py`

```
host = 'YOUR_HOST'
post = YOUR_PORT
```

# Installation & Run

```
$ git clone https://github.com/fake-og-server.git
$ cd fake-og-server
fake-og-server$ pip install -r requirements.txt
fake-og-server$ python service.py
```

# Requirement

- [Flask>=0.11](https://pypi.python.org/pypi/Flask/0.11)
- [beautifulsoup4>=4.4.1](https://pypi.python.org/pypi/beautifulsoup4/4.4.1)

you can install it with `pip install -r requirementes.txt`.

# Reference

- [Open Graph Protocol](http://ogp.me/)
- [CodePen - Input form focus CSS animation](http://codepen.io/hagata/pen/QjdKXy)

# License

MIT