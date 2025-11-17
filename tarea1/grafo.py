import graphviz  # doctest: +NO_EXE

dot = graphviz.Digraph(comment='The Round Table')
#dot  #doctest: +ELLIPSIS
#<graphviz.graphs.Digraph object at 0x...>

# Add nodes and edges:
dot.node('A', 'King Arthur')  # doctest: +NO_EXE
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

# Check the generated source code:
print(dot.source)  # doctest: +NORMALIZE_WHITESPACE +NO_EXE
'''
// The Round Table
digraph {
    A [label="King Arthur"]
    B [label="Sir Bedevere the Wise"]
    L [label="Sir Lancelot the Brave"]
    A -> B
    A -> L
    B -> L [constraint=false]
}
'''

# Save and render the source code (skip/ignore any doctest_mark_exe() lines):
#doctest_mark_exe()  # skip this line
dot.render('./doctest-output/round-table.gv').replace('\\', '/')
#'doctest-output/round-table.gv.pdf'

# Save and render and view the result:
#doctest_mark_exe()  # skip this line
dot.render('./doctest-output/round-table.gv', view=True)  # doctest: +SKIP
#'doctest-output/round-table.gv.pdf'