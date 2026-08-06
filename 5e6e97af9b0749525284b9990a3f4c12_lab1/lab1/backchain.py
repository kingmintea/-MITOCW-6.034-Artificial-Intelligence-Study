from gettext import bind_textdomain_codeset

from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    res = [hypothesis]
    for rule in rules:
        for consequent_ptn in rule.consequent():
            bindings = match(rule.consequent(), hypothesis)
            if bindings is not None:
                p_ant = populate(rule.antecedent(), bindings)
                if isinstance(p_ant, AND):
                    statements = [backchain_to_goal_tree(rules, child) for child in p_ant]
                    res.append(AND(*statements))
                elif isinstance(p_ant, OR):
                    statements = [backchain_to_goal_tree(rules, child) for child in p_ant]
                    res.append(OR(*statements))
                elif isinstance(p_ant, str):
                    res.append(backchain_to_goal_tree(rules, p_ant))
    return simplify(OR(*res))




# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')


