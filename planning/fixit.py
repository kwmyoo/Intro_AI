# Fixit planning problem
# Translation from Dave Touretzky's Ruby implementation fixit.rb
# Jonathan Li, October 2018

from graphplan import *

# Types
WHEEL = 'Wheel'
HUB = 'Hub'
NUT = 'Nut'
CONTAINER = 'Container'
TOOL = 'Tool'

# Instances
i_wheel1 = Instance('wheel1', WHEEL)
i_wheel2 = Instance('wheel2', WHEEL)
i_hub = Instance('hub', HUB)
i_nuts = Instance('nuts', NUT)
i_boot = Instance('boot', CONTAINER)
i_jack = Instance('jack', TOOL)
i_pump = Instance('pump', TOOL)
i_wrench = Instance('wrench', TOOL)


# Variables
v_container = Variable('container', CONTAINER)
v_wheel = Variable('wheel', WHEEL)
v_tool = Variable('tool', TOOL)
v_nut = Variable('nut', NUT)
v_hub = Variable('hub', HUB)

# operators

o_cuss = Operator(
    'cuss',
    # Preconditions
    [],
    # Adds
    [Proposition('not_annoyed')],
    # Deletes
    [] 
)

o_open = Operator(
    'open',
    # Preconditions
    [Proposition('not_open', v_container)],
    # Adds
    [Proposition('open', v_container)],
    # Deletes
    [Proposition('not_open', v_container)]
)

o_close = Operator(
    'close',
    # Preconditions
    [Proposition('open', v_container)],
    # Adds
    [Proposition('not_open', v_container)],
    # Deletes
    [Proposition('open', v_container)]
)

o_fetch_tool = Operator(
    'fetch_tool',
    # Preconditions
    [Proposition('in', v_tool, v_container),
     Proposition('open', v_container)],
    # Adds
    [Proposition('have', v_tool)],
    # Deletes
    [Proposition('in', v_tool, v_container)]
)

o_fetch_wheel = Operator(
    'fetch_wheel',
    # Preconditions
    [Proposition('in', v_wheel, v_container),
     Proposition('open', v_container)],
    # Adds
    [Proposition('have', v_wheel)],
    # Deletes
    [Proposition('in', v_wheel, v_container)]
)

o_put_away_tool = Operator(
    'put_away_tool',
    # Preconditions
    [Proposition('have', v_tool),
     Proposition('open', v_container)],
    # Adds
    [Proposition('in', v_tool, v_container)],
    # Deletes
    [Proposition('have', v_tool)]
)


o_put_away_wheel = Operator(
    'put_away_wheel',
    # Preconditions
    [Proposition('have', v_wheel),
     Proposition('open', v_container)],
    # Adds
    [Proposition('in', v_wheel, v_container)],
    # Deletes
    [Proposition('have', v_wheel)]
)

o_loosen = Operator(
    'loosen',
    # Preconditions
    [Proposition('have', i_wrench),
     Proposition('tight', v_nut, v_hub),
     Proposition('on_ground', v_hub)],
    # Adds
    [Proposition('loose', v_nut, v_hub)],
    # Deletes
    [Proposition('tight', v_nut, v_hub)]
)

o_tighten = Operator(
    'tighten',
    # Preconditions
    [Proposition('have', i_wrench),
     Proposition('loose', v_nut, v_hub),
     Proposition('on_ground', v_hub)],
    # Adds
    [Proposition('tight', v_nut, v_hub)],
    # Deletes
    [Proposition('loose', v_nut, v_hub)]
)

o_jack_up = Operator(
    'jack_up',
    # Preconditions
    [Proposition('on_ground', v_hub),
     Proposition('have', i_jack)],
    # Adds
    [Proposition('not_on_ground', v_hub)],
    # Deletes
    [Proposition('have', i_jack),
     Proposition('on_ground', v_hub)]
)    

o_jack_down = Operator(
    'jack_down',
    # Preconditions
    [Proposition('not_on_ground', v_hub)],
    # Adds
    [Proposition('on_ground', v_hub),
     Proposition('have', i_jack)],
    # Deletes
    [Proposition('not_on_ground', v_hub)]
)

o_undo = Operator(
    'undo',
    # Preconditions
    [Proposition('not_on_ground', v_hub),
     Proposition('not_unfastened', v_hub),
     Proposition('have', i_wrench),
     Proposition('loose', v_nut, v_hub)],
    # Adds
    [Proposition('have', v_nut),
     Proposition('unfastened', v_hub)],
    # Deletes
    [Proposition('on', v_nut, v_hub),
     Proposition('loose', v_nut, v_hub),
     Proposition('not_unfastened', v_hub)]
)

o_do_up = Operator(
    'do_up',
    # Preconditions
    [Proposition('have', i_wrench),
     Proposition('unfastened', v_hub),
     Proposition('not_on_ground', v_hub),
     Proposition('have', v_nut)],
    # Adds
    [Proposition('loose', v_nut, v_hub),
     Proposition('not_unfastened', v_hub)],
    # Deletes
    [Proposition('have', v_nut),
     Proposition('unfastened', v_hub)]
)

o_remove_wheel = Operator(
    'remove_wheel',
    # Preconditions
    [Proposition('not_on_ground', v_hub),
     Proposition('on', v_wheel, v_hub),
     Proposition('unfastened', v_hub)],
    # Adds
    [Proposition('have', v_wheel),
     Proposition('free', v_hub)],
    # Deletes
    [Proposition('on', v_wheel, v_hub)]
)

o_put_on_wheel = Operator(
    'put_on_wheel',
    # Preconditions
    [Proposition('have', v_wheel),
     Proposition('free', v_hub),
     Proposition('unfastened', v_hub),
     Proposition('not_on_ground', v_hub)],
    # Adds
    [Proposition('on', v_wheel, v_hub)],
    # Deletes
    [Proposition('have', v_wheel),
     Proposition('free', v_hub)]
)

o_inflate = Operator(
    'inflate',
    # Preconditions
    [Proposition('have', i_pump),
     Proposition('not_inflated', v_wheel),
     Proposition('intact', v_wheel)],
    # Adds
    [Proposition('inflated', v_wheel)],
    # Deletes
    [Proposition('not_inflated', v_wheel)]
)

problem = PlanningProblem(
    'fixit_problem',
    # Instances
    [i_wheel1, i_wheel2, i_hub, i_nuts, i_boot, i_jack, i_pump, i_wrench],
    # Operators
    [o_cuss, o_open, o_close, o_fetch_tool, o_fetch_wheel, o_put_away_tool,
     o_put_away_wheel, o_loosen, o_tighten, o_jack_up, o_jack_down, o_undo,
     o_do_up, o_remove_wheel, o_put_on_wheel, o_inflate],
    # Initial state
    [Proposition('not_open', i_boot),
     Proposition('intact', i_wheel2),
     Proposition('in', i_jack, i_boot),
     Proposition('in', i_pump, i_boot),
     Proposition('in', i_wheel2, i_boot),
     Proposition('in', i_wrench, i_boot),
     Proposition('on', i_wheel1, i_hub),
     Proposition('on_ground', i_hub),
     Proposition('tight', i_nuts, i_hub),
     Proposition('not_inflated', i_wheel2),
     Proposition('not_unfastened', i_hub)],
    # Goals
    [Proposition('not_open', i_boot),
     Proposition('in', i_jack, i_boot),
     Proposition('in', i_pump, i_boot),
     Proposition('in', i_wheel1, i_boot),
     Proposition('in', i_wrench, i_boot),
     Proposition('tight', i_nuts, i_hub),
     Proposition('inflated', i_wheel2),
     Proposition('on', i_wheel2, i_hub)])

problem.solve()
problem.display()
#problem.dump()
