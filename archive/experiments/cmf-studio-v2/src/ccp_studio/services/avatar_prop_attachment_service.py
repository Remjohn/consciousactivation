from __future__ import annotations

from ccp_studio.contracts.avatar_performance import AvatarPropAttachmentSpec, PropAttachmentSocket


class AvatarPropAttachmentService:
    def create_socket(self, socket_name: str, bone_name: str, offset_x: float = 0.0, offset_y: float = 0.0) -> PropAttachmentSocket:
        return PropAttachmentSocket(socket_name=socket_name, bone_name=bone_name, offset_x=offset_x, offset_y=offset_y)

    def attach_prop(self, *, prop_ref: str, socket: PropAttachmentSocket, purpose: str, sfl_function: str) -> AvatarPropAttachmentSpec:
        return AvatarPropAttachmentSpec(prop_ref=prop_ref, socket=socket, purpose=purpose, sfl_function=sfl_function)
