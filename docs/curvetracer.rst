Curve tracer
================
..  [[[cog
..  name = 'curvetracer'
..  ]]]
..  [[[end]]]


known problems:
 - noisy
 - slow
 
http://en.wikipedia.org/wiki/Curve_tracer

http://en.wikipedia.org/wiki/Current%E2%80%93voltage_characteristic

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
           |                              |           |         |pin_rail=D10|    
           '-----------------------------------------------------------------'    
                  |  100k        MC33201  |        Vin|     Vout|     |    
                  |  ___            |\    |           |         |     |    
                  '-|___|--o--------|+\   |     ___   |  .---.  |     |    
                           |        |  >--o----|___|--o--| X |--o-----'    
                          ---      -|-/   |           |  '---'  |    
                     100n ---     | |/    |   R=120  ---       ---    
                           |      |       |          --- 100n  --- 100n    
                                  |       |           |         |    
                          GND     '-------'          GND       GND    
                                        Vamp                      

..  [[[end]]]



..  [[[cog
..  doc.plots(cog, name, ['IV_curve_plot'])
..  ]]]

IV curve plot
------------------------------


1N4002
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/1N4002.zip')


1N4148
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/1N4148.zip')


BZX55C 2V7
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/BZX55C_2V7.zip')


open
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/open.zip')


red LED
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/red_LED.zip')


short
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('IV_curve_plot').embed('data/curvetracer/short.zip')


analog value time plot
------------------------------


1N4002
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/1N4002.zip')


1N4148
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/1N4148.zip')


BZX55C 2V7
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/BZX55C_2V7.zip')


open
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/open.zip')


red LED
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/red_LED.zip')


short
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('curvetracer').plot('analog_value_time_plot').embed('data/curvetracer/short.zip')

..  [[[end]]]
   



