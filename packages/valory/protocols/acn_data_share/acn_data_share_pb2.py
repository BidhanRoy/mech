# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: acn_data_share.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x14\x61\x63n_data_share.proto\x12 aea.valory.acn_data_share.v0_1_0"\xb8\x01\n\x13\x41\x63nDataShareMessage\x12W\n\x04\x64\x61ta\x18\x05 \x01(\x0b\x32G.aea.valory.acn_data_share.v0_1_0.AcnDataShareMessage.Data_PerformativeH\x00\x1a\x38\n\x11\x44\x61ta_Performative\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\tB\x0e\n\x0cperformativeb\x06proto3'
)


_ACNDATASHAREMESSAGE = DESCRIPTOR.message_types_by_name["AcnDataShareMessage"]
_ACNDATASHAREMESSAGE_DATA_PERFORMATIVE = _ACNDATASHAREMESSAGE.nested_types_by_name[
    "Data_Performative"
]
AcnDataShareMessage = _reflection.GeneratedProtocolMessageType(
    "AcnDataShareMessage",
    (_message.Message,),
    {
        "Data_Performative": _reflection.GeneratedProtocolMessageType(
            "Data_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _ACNDATASHAREMESSAGE_DATA_PERFORMATIVE,
                "__module__": "acn_data_share_pb2"
                # @@protoc_insertion_point(class_scope:aea.valory.acn_data_share.v0_1_0.AcnDataShareMessage.Data_Performative)
            },
        ),
        "DESCRIPTOR": _ACNDATASHAREMESSAGE,
        "__module__": "acn_data_share_pb2"
        # @@protoc_insertion_point(class_scope:aea.valory.acn_data_share.v0_1_0.AcnDataShareMessage)
    },
)
_sym_db.RegisterMessage(AcnDataShareMessage)
_sym_db.RegisterMessage(AcnDataShareMessage.Data_Performative)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _ACNDATASHAREMESSAGE._serialized_start = 59
    _ACNDATASHAREMESSAGE._serialized_end = 243
    _ACNDATASHAREMESSAGE_DATA_PERFORMATIVE._serialized_start = 171
    _ACNDATASHAREMESSAGE_DATA_PERFORMATIVE._serialized_end = 227
# @@protoc_insertion_point(module_scope)
