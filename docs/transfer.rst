Voltage Transfer Curve
=========================
..  [[[cog
..  name = 'transfer'
..  ]]]
..  [[[end]]]


http://en.wikipedia.org/wiki/Inverter_%28logic_gate%29#Performance_measurement

..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

           .-----------------------------------------------------------------.    
           |                         Arduino                                 |    
           |                                    pin_x_in=A2                  |    
           |                                                                 |    
           |                         pin_amp_out=A1   |                      |    
           |  pin_pwm=D9                              |    pin_x_out=A3      |    
           |                              |           |         |            |    
           '-----------------------------------------------------------------'    
                  |  100k        MC33201  |Vamp       |Vin      |Vout         
                  |  ___            |\    |           |         |         
                  '-|___|--o--------|+\   |     ___   |  .---.  |         
                           |        |  >--o----|___|--o--| X |--o    
                          ---      -|-/   |           |  '---'  |    
                     100n ---     | |/    |   R=120  ---       ---    
                           |      |       |          --- 100n  --- 100n    
                                  |       |           |         |    
                          GND     '-------'          GND       GND    
                              
                                                              

..  [[[end]]]



..  [[[cog
..  doc.plots(cog, name, ['transfer_plot'])
..  ]]]

transfer plot
------------------------------


7486PC
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/7486PC.zip')


74LS00
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/74LS00.zip')


CD4011
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/CD4011.zip')


K155LA3
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/K155LA3.zip')


KS74HCTLS14
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/KS74HCTLS14.zip')


short
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('transfer_plot').embed('data/transfer/short.zip')


analog value time plot
------------------------------


7486PC
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/7486PC.zip')


74LS00
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/74LS00.zip')


CD4011
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/CD4011.zip')


K155LA3
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/K155LA3.zip')


KS74HCTLS14
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/KS74HCTLS14.zip')


short
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('transfer').plot('analog_value_time_plot').embed('data/transfer/short.zip')

..  [[[end]]]
   



