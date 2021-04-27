from logic import *


############################################################
# Problem 1: propositional logic
# Convert each of the following natural language sentences into a propositional
# logic formula.  See rainWet() in examples.py for a relevant example.

# Sentence: "If it's summer and we're in California, then it doesn't rain."
def formula1a():
    # Predicates to use:
    Summer = Atom('Summer')  # whether it's summer
    California = Atom('California')  # whether we're in California
    Rain = Atom('Rain')  # whether it's raining
    # BEGIN_YOUR_CODE
    return Implies(And(Summer, California), Not(Rain))
    # END_YOUR_CODE


# Sentence: "It's wet if and only if it is raining or the sprinklers are on."
def formula1b():
    # Predicates to use:
    Rain = Atom('Rain')  # whether it is raining
    Wet = Atom('Wet')  # whether it it wet
    Sprinklers = Atom('Sprinklers')  # whether the sprinklers are on
    # BEGIN_YOUR_CODE
    return And(Implies(And(Not(Rain), Not(Sprinklers)), Not(Wet)), Implies(Or(Rain, Sprinklers), Wet))
    # END_YOUR_CODE


# Sentence: "Either it's day or night (but not both)."
def formula1c():
    # Predicates to use:
    Day = Atom('Day')  # whether it's day
    Night = Atom('Night')  # whether it's night
    # BEGIN_YOUR_CODE
    return Xor(Day, Night)
    # END_YOUR_CODE


############################################################
# Problem 2: first-order logic

# Sentence: "Every person has a mother."
def formula2a():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person

    def Mother(x, y): return Atom('Mother', x, y)  # whether x's mother is y

    # Note: You do NOT have to enforce that the mother is a "person"
    # BEGIN_YOUR_CODE
    return Forall('$x', Implies(Person('$x'), Exists('$y', Mother('$x', '$y'))))
    # END_YOUR_CODE


# Sentence: "At least one person has no children."
def formula2b():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person

    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y

    # Note: You do NOT have to enforce that the child is a "person"
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Exists('$x', And(Person('$x'), Not(Exists('$y', Child('$x', '$y')))))
    # END_YOUR_CODE


# Return a formula which defines Daughter in terms of Female and Child.
# See parentChild() in examples.py for a relevant example.
def formula2c():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female

    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y

    def Daughter(x, y): return Atom('Daughter', x, y)  # whether x has a daughter y

    # BEGIN_YOUR_CODE
    return Forall('$x', Forall('$y', Equiv((And(Female('$y'), Child('$x', '$y'))), Daughter('$x', '$y'))))
    # END_YOUR_CODE


# Return a formula which defines Grandmother in terms of Female and Parent.
# Note: It is ok for a person to be her own parent
def formula2d():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female

    def Parent(x, y): return Atom('Parent', x, y)  # whether x has a parent y

    def Grandmother(x, y): return Atom('Grandmother', x, y)  # whether x has a grandmother y

    # BEGIN_YOUR_CODE
    return Forall('$x',
                  Forall('$y',
                         Equiv(Grandmother('$x', '$y'), And(Female('$y'),
                                                            Exists('$z',
                                                                   And(Parent('$x', '$z'), Parent('$z', '$y')))))))
    # END_YOUR_CODE


############################################################
# Problem 3: Liar puzzle

# Facts:
# 0. John: "It wasn't me!"
# 1. Susan: "It was Nicole!"
# 2. Mark: "No, it was Susan!"
# 3. Nicole: "Susan's a liar."
# 4. Exactly one person is telling the truth.
# 5. Exactly one person crashed the server.
# Query: Who did it?
# This function returns a list of 6 formulas corresponding to each of the
# above facts.
# Hint: You might want to use the Equals predicate, defined in logic.py.  This
# predicate is used to assert that two objects are the same.
# In particular, Equals(x,x) = True and Equals(x,y) = False iff x is not equal to y.
def liar():
    def TellTruth(x): return Atom('TellTruth', x)

    def CrashedServer(x): return Atom('CrashedServer', x)

    john = Constant('john')
    susan = Constant('susan')
    nicole = Constant('nicole')
    mark = Constant('mark')
    formulas = []
    # We provide the formula for fact 0 here.
    formulas.append(Equiv(TellTruth(john), Not(CrashedServer(john))))
    # You should add 5 formulas, one for each of facts 1-5.
    # BEGIN_YOUR_CODE
    formulas.append(Equiv(TellTruth(susan), CrashedServer(nicole)))
    formulas.append(Equiv(TellTruth(mark), CrashedServer(susan)))
    formulas.append(Equiv(TellTruth(nicole), Not(TellTruth(susan))))

    # 把下面这两个式子合并一下即可得到 fact4 和 fact5 (注意这里不能直接And连接两个式子，因为在两个式子中共用了'$x', 因此需要将第二个式子插进第一个式子中)
    # Exists('$x', And(TellTruth('$x'), Forall('$y', Implies(Not(Equals('$y', '$x')), Not(TellTruth('$y'))))))
    # Not(Exists('$z', And(Not(Equals('$x', '$z')), And(TellTruth('$z'), Forall('$k', Implies(Not(Equals('$k', '$z')), Not(TellTruth('$k'))))))))

    formulas.append(
        Exists('$x',
               And(TellTruth('$x'), Forall('$y',
                                            And(Implies(Not(Equals('$y', '$x')), Not(TellTruth('$y'))),
                                                    Not(Exists('$z',
                                                               And(Not(Equals('$x', '$z')), And(TellTruth('$z'),
                                                                                                Forall('$k',
                                                                                                       Implies(Not(Equals('$k', '$z')), Not(TellTruth('$k'))))))))))))
    )
    formulas.append(
        Exists('$x',
               And(CrashedServer('$x'), Forall('$y',
                                           And(Implies(Not(Equals('$y', '$x')), Not(CrashedServer('$y'))),
                                               Not(Exists('$z',
                                                          And(Not(Equals('$x', '$z')), And(CrashedServer('$z'),
                                                                                           Forall('$k',
                                                                                                  Implies(Not(Equals('$k', '$z')), Not(CrashedServer('$k'))))))))))))
    )
    # END_YOUR_CODE
    query = CrashedServer('$x')
    return (formulas, query)


############################################################
# Problem 4: Odd and even integers

# Return the following 6 laws:
# 0. Each number $x$ has a unique successor, which is not equal to $x$.
# 1. Each number is either even or odd, but not both.
# 2. The successor number of an even number is odd.
# 3. The successor number of an odd number is even.
# 4. For every number $x$, the successor of $x$ is larger than $x$.
# 5. Larger is a transitive property: if $x$ is larger than $y$ and $y$ is
#    larger than $z$, then $x$ is larger than $z$.
# Query: For each number, there exists an even number larger than it.
def ints():
    def Even(x): return Atom('Even', x)  # whether x is even

    def Odd(x): return Atom('Odd', x)  # whether x is odd

    def Successor(x, y): return Atom('Successor', x, y)  # whether x's successor is y

    def Larger(x, y): return Atom('Larger', x, y)  # whether x is larger than y

    # Note: all objects are numbers, so we don't need to define Number as an
    # explicit predicate.
    # Note: pay attention to the order of arguments of Successor and Larger.
    # Populate |formulas| with the 6 laws above and set |query| to be the
    # query.
    # Hint: You might want to use the Equals predicate, defined in logic.py.  This
    # predicate is used to assert that two objects are the same.
    formulas = []
    query = None
    # We provide the formula for fact 0 here.
    formulas.append(
        Forall('$x',
               Exists('$y', And(And(Not(Equals('$x', '$y')), Successor('$x', '$y')),
                                Forall('$z', Or(Equals('$y', '$z'), Not(Successor('$x', '$z'))))))))
    # BEGIN_YOUR_CODE
    formulas.append(Forall('$x', Xor(Even('$x'), Odd('$x'))))
    formulas.append(
        Forall('$x', Forall('$y', Implies(And(Even('$x'), Successor('$x', '$y')), Odd('$y'))))
    )
    formulas.append(
        Forall('$x', Forall('$y', Implies(And(Odd('$x'), Successor('$x', '$y')), Even('$y'))))
    )
    formulas.append(
        Forall('$x', Forall('$y', Implies(Successor('$x', '$y'), Larger('$y', '$x'))))
    )
    formulas.append(
        Forall('$x',
               Forall('$y',
                      Forall('$z',
                             Implies(And(Larger('$x', '$y'), Larger('$y', '$z')), Larger('$x', '$z')))))
    )
    # END_YOUR_CODE
    query = Forall('$x', Exists('$y', And(Even('$y'), Larger('$y', '$x'))))
    return (formulas, query)
