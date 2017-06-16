Installing Insights
===================

Here are some handy instructions on installing Insights and running these
rules.

Requirements
------------

* Python 2.7
* Virtualenv

Clone the source code
---------------------

```
mkdir insights
cd insights
git clone https://RedhatInsights/insights-core.git
git clone https://RedHatInsights/insights-plugins-demo.git
```
Set up the VirtualEnv
---------------------

```
virtualenv .
source bin/activate
pip install -e insights-core[develop]
pip install -e insights-plugins-demo
```

