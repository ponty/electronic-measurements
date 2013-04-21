Op-amp I/O range
=============================
..  [[[cog
..  name = 'swing'
..  ]]]
..  [[[end]]]




..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

 .-----------------.    
 |     Arduino     |    
 |                 |    
 |                 |              Vminus    
 |pin_in_minus=A1  | --------o-----------.    
 |                 |         |           |          R2=100000 
 |                 |         |    |\|    |  R1=10000          
 |                 | 100k    '----|-\    |   ___        ___    
 |                 |  ___         |  >---o--|___|--o---|___|---.    
 |pin_pwm_minus=D10|-|___|---o----|+/              |           |    
 |                 |         |    |/|              |           |    
 |                 |        ---                    |           |    
 |                 |   100n ---  MC33201           |           |    
 |                 |         |                     |           |    
 |                 |         |                     |           |    
 |                 |        ===                    |   |\|     |    
 |                 | 100k   GND                    '---|-\     |    
 |                 |  ___              Vplus           |  >----o    
 | pin_pwm_plus=D9 |-|___|--o------o-------------------|+/     |    
 |                 |        |      |                   |/|     |    
 |                 |       ---     |                           |    
 |                 |   100n---     |                  unknown  |    
 |                 |        |      |                           |    
 |                 |        |      |                           |    
 |                 |       ===     |                           |    
 |                 |       GND     |                           |    
 |                 |               |                           |    
 |  pin_in_plus=A0 |---------------'                           |    
 |                 |                   Vout                    |    
 |  pin_out=A2     | ----------o---------------------o---------'    
 |                 |    ___    |                     |    
 | pin_load_1=D12  | --|___|---o  Rload_1=47000     --- C3     
 |                 |    ___    |                    --- 1u     
 | pin_load_2=D11  | --|___|---o   Rload_2=4700      |    
 |                 |    ___    |                    ===    
 | pin_load_3=D8   | --|___|- -'   Rload_3=470      GND    
 '-----------------'    
    
C3 is needed if op-amp oscillates (e.g. CA3130)    

..  [[[end]]]



..  [[[cog
..  doc.plots(cog, name, ['input_range_plot','input_range_error_plot','output_swing_plot','output_swing_error_plot'])
..  ]]]

input range plot
------------------------------


CA3130
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/CA3130.zip')


KA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/KA741.zip')


LM318
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/LM318.zip')


MC33201
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/MC33201.zip')


TL071
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/TL071.zip')


uA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_plot').embed('data/swing/uA741.zip')


input range error plot
------------------------------


CA3130
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/CA3130.zip')


KA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/KA741.zip')


LM318
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/LM318.zip')


MC33201
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/MC33201.zip')


TL071
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/TL071.zip')


uA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('input_range_error_plot').embed('data/swing/uA741.zip')


output swing plot
------------------------------


CA3130
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/CA3130.zip')


KA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/KA741.zip')


LM318
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/LM318.zip')


MC33201
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/MC33201.zip')


TL071
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/TL071.zip')


uA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_plot').embed('data/swing/uA741.zip')


output swing error plot
------------------------------


CA3130
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/CA3130.zip')


KA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/KA741.zip')


LM318
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/LM318.zip')


MC33201
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/MC33201.zip')


TL071
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/TL071.zip')


uA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('output_swing_error_plot').embed('data/swing/uA741.zip')


analog value time plot
------------------------------


CA3130
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/CA3130.zip')


KA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/KA741.zip')


LM318
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/LM318.zip')


MC33201
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/MC33201.zip')


TL071
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/TL071.zip')


uA741
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('swing').plot('analog_value_time_plot').embed('data/swing/uA741.zip')

..  [[[end]]]

 
    