from logic2 import *

kb = PropKB()

pitrules = [
    'B11 <=> (P12 | P21)',
    'B12 <=> (P11 | P13 | P22)',
    'B13 <=> (P12 | P14 | P23)',
    'B14 <=> (P13 | P24)',
    'B21 <=> (P11 | P31 | P22)',
    'B22 <=> (P21 | P23 | P12 | P32)',
    'B23 <=> (P22 | P24 | P13 | P33)'
]

for rule in pitrules:
    kb.tell(rule)

kb.tell(expr('~P11'))
kb.tell(expr('~B11'))
#kb.tell(expr('B12'))
#kb.tell(expr('~P12'))
#kb.tell(expr('~B21'))
#kb.tell(expr('~P21'))

pl_resolution(kb, expr('~P12'))
