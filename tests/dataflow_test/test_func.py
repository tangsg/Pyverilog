import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.optimizer import VerilogDataflowOptimizer
from pyverilog.controlflow.controlflow_analyzer import VerilogControlflowAnalyzer
codedir = '../../testcode/'

expected = """\
TOP.RST_X: TOP_RST_X
TOP.md_always0.al_block0.al_if0_ELSE.al_block2.al_functioncall0.inc: (((!TOP_RST_X))? TOP_al_block0_al_block2_al_functioncall0_inc : (((!TOP_RST_X))? (((&TOP_al_block0_al_block2_al_functioncall0_inc))? 'd0 : (((!TOP_RST_X))? (TOP_al_block0_al_block2_al_functioncall0_inc+'d1) : (TOP_cnt+'d1))) : (((&TOP_al_block0_al_block2_al_functioncall0_inc))? (((!TOP_RST_X))? (TOP_al_block0_al_block2_al_functioncall0_inc+'d1) : (TOP_cnt+'d1)) : (((!TOP_RST_X))? (((&(TOP_al_block0_al_block2_al_functioncall0_inc+'d1)))? 'd0 : (((!TOP_RST_X))? (TOP_al_block0_al_block2_al_functioncall0_inc+'d1) : (TOP_cnt+'d1))) : (((&(TOP_cnt+'d1)))? 'd0 : (((!TOP_RST_X))? (TOP_al_block0_al_block2_al_functioncall0_inc+'d1) : (TOP_cnt+'d1)))))))
TOP.md_always0.al_block0.al_if0_ELSE.al_block2.al_functioncall0._rn1_inc: (((!TOP_RST_X))? (TOP_al_block0_al_block2_al_functioncall0__rn1_inc+'d1) : (TOP_cnt+'d1))
TOP.cnt: (((!TOP_RST_X))? 'd0 : (((!TOP_RST_X))? TOP_cnt : (((&TOP_al_block0_al_block2_al_functioncall0_inc))? 'd0 : (((!TOP_RST_X))? (TOP_cnt+'d1) : (TOP_cnt+'d1)))))
TOP.md_always0.al_block0.al_if0_ELSE.al_block2.al_functioncall0.in: (((!TOP_RST_X))? TOP_al_block0_al_block2_al_functioncall0_in : TOP_cnt)
TOP.CLK: TOP_CLK
TOP.md_always0.al_block0.al_if0_ELSE.al_block2.al_functioncall0._rn0_inc: 'd0
"""

def test():
    filelist = [codedir + 'function.v']
    topmodule = 'TOP'
    noreorder = False
    nobind = False
    include = None
    define = None

    analyzer = VerilogDataflowAnalyzer(filelist, topmodule,
                                       noreorder=noreorder,
                                       nobind=nobind,
                                       preprocess_include=include,
                                       preprocess_define=define)
    analyzer.generate()

    directives = analyzer.get_directives()
    instances = analyzer.getInstances()
    terms = analyzer.getTerms()
    binddict = analyzer.getBinddict()

    optimizer = VerilogDataflowOptimizer(terms, binddict)
    optimizer.resolveConstant()

    c_analyzer = VerilogControlflowAnalyzer(topmodule, terms,
                                            binddict,
                                            resolved_terms=optimizer.getResolvedTerms(),
                                            resolved_binddict=optimizer.getResolvedBinddict(),
                                            constlist=optimizer.getConstlist()
                                            )

    output = []
    for tk in sorted(c_analyzer.resolved_terms.keys(), key=lambda x:str(x[0])):
        tree = c_analyzer.makeTree(tk)
        output.append(str(tk) + ': ' + tree.tocode())

    rslt = '\n'.join(output) + '\n'

    print(rslt)
    assert(rslt == expected)

if __name__ == '__main__':
    test()