MCU digital input curve
=========================
..  [[[cog
..  name = 'mcudiginput'
..  ]]]
..  [[[end]]]




..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

           .-----------------------------------------------------------------.    
           |                         Arduino                                 |    
           |                                     pin_an_in=A2                |    
           |                                                                 |    
           |                          pin_amp_out     |  pin_dig_in=D8       |    
           |  pin_pwm=D9                              |        |             |    
           |                              |           |        |             |    
           '-----------------------------------------------------------------'    
                  |  100k        MC33201  |        Ain|        |Din      
                  |  ___            |\    |           |        |            
                  '-|___|--o--------|+\   |     ___   |        |           
                           |        |  >--o----|___|--o--------o       
                          ---      -|-/   |                    |    
                     100n ---     | |/    |     120           --- 1u    
                           |      |       |                   ---    
                                  |       |                    |    
                          GND     '-------'                   GND    
                                        Vamp                      

..  [[[end]]]



..  [[[cog
..  doc.plots(cog, name, ['dig_input_plot'])
..  ]]]

dig input plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('mcudiginput').plot('dig_input_plot').embed('data/mcudiginput/ATmega88.zip')


analog value time plot
------------------------------


ATmega88
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('mcudiginput').plot('analog_value_time_plot').embed('data/mcudiginput/ATmega88.zip')

..  [[[end]]]
   



