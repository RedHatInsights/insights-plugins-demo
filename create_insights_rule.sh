#!/bin/bash

# Create an Insights rule and its associated test.
# Written by Paul Wayper in June 2017.
# This script is released under the GNU General Public License v3.

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <rule_name>"
    exit 1
fi

# Rule names are usually all lower case, with words separated by underscores.
# The error key, which uniquely identifies the result of a rule, is usually
# the same name but in all upper case.  Rules can generate multiple results,
# in which case multiple error keys would be used in the same rule.

rule_name="$1"
error_key=${rule_name^^[a-z]}

rule_path="demo/rules"
test_path="demo/tests"
rule_import="demo.rules"

# Sanity check in case of being run again
if [[ -f $rule_file ]]; then
    echo "Error: rule file '$rule_file' already exists - try another"
    exit 1
fi

# You may like to uncomment this line if you prefer hyphens instead of
# underscores in your git branch names.
# branch_name=$( echo $rule_name | tr _ - )
branch_name=$rule_name

# It's standard practice to create a new branch when working on a rule.
if git branch | grep -q '* master'; then
    echo "Warning: making a new git branch for you."
    git checkout -b "${USER}-${branch_name}"
fi

rule_file="$rule_path/$rule_name.py"
test_file="$test_path/test_$rule_name.py"
USER_NAME=$( getent passwd $USER | cut -d : -f 5 )

# Create the rule file
cat > $rule_file << RULE_EOF
"""
TODO write rule description TODO

Written by $USER_NAME

"""
from insights.core.plugins import make_response, rule
from insights.parsers.TODO_PARSER_MODULE import TODO_PARSER_NAME

ERROR_KEY = '$error_key'


@rule(requires=[TODO_PARSER_NAMES])
def $rule_name(local, shared):
    """
    TODO: explain how this rule works
    """
    TODO_some_info = shared[TODO_PARSER_NAME]

    if TODO_some_info.TODO_reason_this_rule_doesnt_apply():
        return

    if TODO_some_info.TODO_cause_of_problem_detected():
        return make_response(
            ERROR_KEY,
            kcs=KCS,
            TODO_info_key=TODO_information_to_user_about_problem
        )
RULE_EOF

# Create the test file
cat > $test_file << TEST_EOF
from $rule_import import $rule_name
from insights.core.plugins import make_response
from insights.tests import InputData, archive_provider

GOOD_TEST_CONTENT = """
TODO: add content from a system without the problem
"""

BAD_TEST_CONTENT = """
TODO: add content from a system with the problem
"""


@archive_provider($rule_name)
def integration_tests():
    # Test that should pass
    data = InputData("good_test_1")
    data.add('TODO_file_spec', GOOD_TEST_CONTENT)
    yield data, []

    # Test that should fail
    data = InputData("bad_test_1")
    data.add('TODO_file_spec', BAD_TEST_CONTENT)
    expected = make_response(
        $rule_name.ERROR_KEY,
        TODO_info_key=TODO_information_to_user_about_problem
    )
    yield data, [expected]
TEST_EOF

git add $rule_file
git add $test_file
echo "Rule file is: '$rule_file'"
echo "Test file is: '$test_file'"
echo "DO NOT COMMIT YET, you need to do some search and replace first!"
echo "Replace all instances of 'TODO' with meaningful content"
