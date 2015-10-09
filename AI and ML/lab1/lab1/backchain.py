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


def backchain_to_goal_tree(rules, hypothesis,myLeaf = []):
    count = 0
    for i in range(len(rules)):
        bindings = (match(rules[i].consequent()[0],hypothesis))
        if bindings is not None:
            print 'type of bindings',bindings
            andLeaf = AND()
            orLeaf = OR()
            for x in range(len(rules[i].antecedent())):
                print 'in antecedent.....',rules[i].antecedent()[x]
                node = populate((rules[i].antecedent()[x]),bindings)
                if type(rules[i].antecedent()) == AND:
                    andLeaf.append(populate((rules[i].antecedent()[x]),bindings))
                    myLeaf.append(simplify(andLeaf))
                    print 'andLeaf', andLeaf
                if type(rules[i].antecedent()) == OR:
                    orLeaf.append(populate((rules[i].antecedent()[x]),bindings))
                    myLeaf.append(simplify(orLeaf))
                    print 'orLeaf',orLeaf
                
                
                disnode = backchain_to_goal_tree(rules,node)
        else:
            print 'hypothesis'
            #myLeaf.append(hypothesis)
             
    return simplify(myLeaf)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
myLeaf = []
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
