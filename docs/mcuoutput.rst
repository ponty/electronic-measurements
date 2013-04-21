MCU output pin IV curve
=======================
..  [[[cog
..  name = 'mcuoutput'
..  ]]]
..  [[[end]]]


..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

           .-----------------------------------------------------------------.    
           |                         Arduino                                 |    
           |                                                                 |    
           |                                                                 |    
           |                         pin_amp_out=A1                          |    
           |  pin_pwm=D9                              pin_out_an=A3          |    
           |                              |                 |pin_out_dig=D10 |    
           '-----------------------------------------------------------------'    
                  |  68k       MC33201    |                 |     |    
                  |  ___            |\    |                 |     |    
                  '-|___|--o--------|+\   |     ___         |     |    
                           |        |  >--o----|___|--------o-----'    
                          ---      -|-/   |    
                     100n ---     | |/    |   R=120   
                           |      |       |    
                                  |       |    
                          GND     '-------'    
                                        Vamp              Vout     

..  [[[end]]]


..  [[[cog
..  doc.plots(cog, name, ['io_iv_plot'])
..  ]]]

io iv plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('mcuoutput').plot('io_iv_plot').embed('data/mcuoutput/ATmega88.zip')


analog value time plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('mcuoutput').plot('analog_value_time_plot').embed('data/mcuoutput/ATmega88.zip')

..  [[[end]]]

