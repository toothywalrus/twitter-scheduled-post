import sys

from rest_framework import serializers

import utils


for name in utils.get_info_names():
    class Meta:
        model = utils.get_model_class(name)

    gen_class = type(utils.get_serializer_name(name),
                     (serializers.ModelSerializer, ),
                     {'Meta': Meta})

    setattr(sys.modules[__name__], gen_class.__name__, gen_class)
