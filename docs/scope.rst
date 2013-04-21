Oscilloscope
================
..  [[[cog
..  name = 'scope'
..  ]]]
..  [[[end]]]

known problems:
 - very slow

..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

        .-------------------.    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |           input    
        |         pin=A0 -------------------    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        '-------------------'    

..  [[[end]]]

..  [[[cog
..  doc.plots(cog, name, ['voltage_time_plot'])
..  ]]]

voltage time plot
------------------------------


noise
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('scope').plot('voltage_time_plot').embed('data/scope/noise.zip')


analog value time plot
------------------------------


noise
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('scope').plot('analog_value_time_plot').embed('data/scope/noise.zip')

..  [[[end]]]
 


 
    