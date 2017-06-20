# Demo rules for Insights

This is a basic rule repository for Insights.  The contents are simple but they
are intended to provide a basic demonstration of how to write rules and tests.

Obviously, Red Hat doesn't provide support for using these rules, but patches
and suggestions are welcome if you can figure out how to provide them.

---

## Installing Insights
Here are some handy instructions on installing Insights and running these
rules.

### Requirements

* Python 2.7
* Virtualenv

### Clone the source code
```bash
mkdir insights
cd insights
git clone https://github.com/RedhatInsights/insights-core.git
git clone https://github.com/RedHatInsights/insights-plugins-demo.git
```
### Set up the VirtualEnv

```bash
virtualenv .
source bin/activate
```

If you've only got Python 2.7 available, you will need to install Sphinx
version 1.6.1 as follows:

```
pip install Sphinx==1.6.1
```

Now install the rest of Insights including the development tools (because
you want to write and test rules):

```
pip install -e insights-core[develop]
pip install -e insights-plugins-demo
```

### Does your environment work?

You should now be able to validate the environment by doing:

```
cd insights-plugins-demo
py.test demo
```

Which will output something along the lines of:

```
$ py.test demo
============================= test session starts ============================
platform linux2 -- Python 2.7.5, pytest-3.0.6, py-1.4.34, pluggy-0.4.0
rootdir: /tmp/insights-demo/insights-plugins-demo, inifile: setup.cfg
plugins: cov-2.4.0
collected 2 items

demo/tests/integration.py ..

========================== 2 passed in 0.09 seconds ==========================
```

You can likewise validate the entire Insights core framework with:

```
cd insights-core
py.test insights
```

## We also have lovely documentation!

Insights Core comes with a lot of documentation about the framework -
particularly the parsers and combiners that rules use to gather data.  It can
be found over on [readthedocs](http://insights-core.readthedocs.io/en/latest/),
or you can build it using:

```
cd insights-core/docs
make html
```

You can then open ``insights-core/docs/_build/html/index.html`` in your
favourite browser to read more about the framework.
