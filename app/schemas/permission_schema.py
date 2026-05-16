from pydantic import BaseModel


class PermissionAddSchema(BaseModel):
    role_id: int
    resource_id: int
    can_read: bool
    can_all_read: bool
    can_create: bool
    can_all_create: bool
    can_update: bool
    can_all_update: bool
    can_delete: bool
    can_all_delete: bool


class PermissionEditSchema(BaseModel):
    id: int
    can_read: bool
    can_all_read: bool
    can_create: bool
    can_all_create: bool
    can_update: bool
    can_all_update: bool
    can_delete: bool
    can_all_delete: bool
