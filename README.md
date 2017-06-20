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
pip install -e insights-core[develop]
pip install -e insights-plugins-demo
```

