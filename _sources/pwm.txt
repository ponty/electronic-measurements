PWM loopback test
=============================
..  [[[cog
..  name = 'pwm'
..  ]]]
..  [[[end]]]

 
..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

        .-------------------.    
        |                   |    
        |                   |    
        |      pin_in=A0    )------------.    
        |                   |            |    
        |                   |     100k   |    
        |                   |     ___    |    
        |      pin_pwm=D9   )----|___|---o    
        |                   |            |    
        |                   |            |    
        |                   |           ---    
        |                   |           ---  100n    
        |                   |            |    
        |          GND      )------------'    
        |                   |    
        |                   |    
        '-------------------'    

..  [[[end]]]


..  [[[cog
..  doc.plots(cog, name, ['transfer_error_plot'])
..  ]]]

transfer error plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('pwm').plot('transfer_error_plot').embed('data/pwm/ATmega88.zip')


analog value time plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('pwm').plot('analog_value_time_plot').embed('data/pwm/ATmega88.zip')

..  [[[end]]]




    