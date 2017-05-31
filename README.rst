Plivo Framework
-----

Description
~~~~~~~~~~~

Plivo Framework is an open source telephony application prototyping framework you can use to create
a wide variety of applications(IVRs, Billing System, Voicemail, Click to Call etc)
in a simple and extensible manner, using any web language you know.


Documentation
~~~~~~~~~~~~~~

See `Plivo Documentation <http://docs.plivo.org>`_ for more information.

Cambios

  * Se implementa [plivo-uploader] para envio y retroalimentacion de grabaciones con S3.

<Record/>
~~~~~~~~~~~~~~~~

Se agregan los siguientes atributos:

  * *awsRegion* :  especificar la region aws
  * *awsBucket* : especificar el bucket aws
  * *recordSession* : grabar en fondo
  * *startOnDialAnswer* : iniciar grabacion al contestar
    

/Call
~~~~~~~~~~~

  * *ringTimeout*: en segundos

/CancelRequest
metodo: POST

  * *RequestUUID* : UUID

/Request/<request_uuid>
~~~~~~~~~~~~~

Cancela llamada antes de ser contestada

/HangupConference

metodo: POST

   * *ConferenceName* : nombre de conferencia
  
License
~~~~~~~~

Copyright (c) 2011 Plivo Inc <hello@plivo.com>

Plivo Framework is distributed under the terms of the Mozilla Public License Version 1.1, see `LICENSE`.
