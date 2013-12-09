Frequency meter
===============
..  [[[cog
..  name = 'fmeter'
..  ]]]
..  [[[end]]]


..  [[[cog
..  from elme import doc
..  doc.schematic(cog, name)
..  ]]]

Schematic::

        .-------------------.    
        |  Arduino          |    
        |                   |    
        |                   |    
        |                   |    
        |                   |    
        |                   |           input    
        |          D5   -------------------    
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
..  doc.plots(cog, name, ['frequency_time_plot'], auto_time_plot=0)
..  ]]]

frequency time plot
------------------------------


PWM 1220Hz
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_1220Hz.zip')


PWM 305Hz
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_305Hz.zip')


PWM 76Hz
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_76Hz.zip')


PWM 76Hz G100ms
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_76Hz_G100ms.zip')


PWM 78125Hz
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_78125Hz.zip')


PWM 9765Hz
++++++++++++++++++++++++++++++++++

.. plot::

    from elme.project import Project
    Project('fmeter').plot('frequency_time_plot').embed('data/fmeter/PWM_9765Hz.zip')

..  [[[end]]]
 


 
    