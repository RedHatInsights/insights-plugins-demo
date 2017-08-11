A Guided Tour of the Insights Demo Plugins
==========================================

You've got Insights installed, and you've been able to test it by running
the Insights CLI with something like:

```:bash
insights-cli / --plugin-modules demo
```

Now you're keen to learn how to write rules, by looking at how some of these
rules are written.  We'll assume you've read the 'Insights processing
background' description in ``MORE_INFO.md``.  So let's tour around the
rules in this repository and see what we can learn.

Simple rules
------------

These rules draw information from a single Parser and their logic is fairly
straightforward.  They have one 'condition', so they express that simply as
a rule.

### `localhost_in_hosts`

This rule checks that `localhost` is defined in your `/etc/hosts` file.

This uses the `Hosts` parser, which provides a simple dictionary of all the
host names seen in the `all_names` property.

*What we learned* : use a parser's properties rather than searching the
data it contains.

### `smartctl_reallocated_sectors`

This rule reports on any drive that has the reallocated sector count greater
than zero in its `SMART` data, which is a sign that the drive is nearing its
end of life.

The `SMARTctl` parser is based on the `smartctl` spec, which is based on a
PatternMatch spec class.  This means that the the `shared[SMARTctl]` entry
is actually a *list* of one or more `SMARTctl` objects.  In order to look at
every drive, you need to loop through the objects in that list.

*What we learned* : parsers based on PatternSpecs will produce a list of
parser results, one per input file, so you have to loop over them.

### `high_swap_usage`

This rule detects when the amount of used swap memory (total - (free + cached))
is greater than 50%.



Intermediate rules
------------------

These rules draw from multiple parsers, so they use **condition**s to separate
out each part of the rule's logic.

Complex rules
-------------

These rules draw data from multiple parsers, and use one or more conditions.
They may use advanced features of the parser in order to determine rule
conditions. In addition, they try to derive information to tell the user how
to fix the detected problem.

### `rsyslog_dropping_messages`

This rule detects when rsyslog is dropping messages from particular processes,
and suggests a possible increased configuration value to capture these bursts.

This involves
