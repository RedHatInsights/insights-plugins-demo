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
version 1.6.1 and cryptography version 2.0 as follows:

```
pip install Sphinx==1.6.1
pip install cryptography==2.0
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

---

# What is this rule repository for?

There are three main objectives for this rule repository:

1. Copy it to create your own repository of rules!
2. Read the existing rules to see how to write your own.
3. Test your Insights set up with rules that are know to work.

All good.  Here are a few things that it is not:

a. A comprehensive test of every feature and corner of the core framework.
   It has its own internal test suite.
b. Any kind of 'definitive' collection of rules.  We'd much rather people
   publish their own rule sets.
c. A 'best practice' guide for how to write rules or what rules to write.
   Treat it more like a tutorial than a comprehensive manual.

Of course, we still welcome any bug fixes or suggestions for improvement :-)

# OK, so how do I use this in practice?

Firstly, you need to install the components of Insights.  The easiest way to
do that is to use the Insights Installer:

https://github.com/PaulWay/insights-installer

The install script in that repository will install the Insights core, as well
as this rule repository.

Once installed, you can then run the Insights CLI, giving it this demo rule
set as the rule module to use:

```bash
source bin/activate
insights-cli / --plugin-modules demo.rules
```
